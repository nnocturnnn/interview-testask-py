import os

import jwt
import requests
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .misc import check_image_format  # noqa: F401
from .misc import check_file, check_image_size, scale_image, upload_to_bucket
from .models import Attachment, Comment, Like  # noqa: F401


def base_view(request):
    sort = request.GET.get("sort", "date_added")
    direction = request.GET.get("direction", "desc")
    valid_sort_fields = ["user_name", "email", "date_added"]
    sort = "date_added" if sort not in valid_sort_fields else sort
    order_by_field = sort if direction == "asc" else f"-{sort}"
    comments_list = Comment.objects.prefetch_related("attachments").order_by(
        order_by_field
    )  # noqa: E501
    paginator = Paginator(comments_list, 25)

    page_number = request.GET.get("page")
    comments = paginator.get_page(page_number)
    context = {
        "comments": comments,
        "jwt_token": request.session.get("jwt_token", ""),
    }  # noqa: E501
    return render(request, "index.html", context)


@require_http_methods(["POST"])
def comment_add(request):
    recaptcha_response = request.POST.get("g-recaptcha-response")
    data = {
        "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
        "response": recaptcha_response,
    }
    result = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=data
    )  # noqa: E501
    result_json = result.json()

    if not result_json.get("success"):
        return JsonResponse({"error": "Invalid CAPTCHA"}, status=400)

    # Retrieve the JWT token from the session
    token = request.session.get("jwt_token")
    if not token:
        return HttpResponseForbidden("Authentication required")

    try:
        # Decode the token to get user information
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return HttpResponseForbidden("Invalid token")

        # Retrieve and process the comment data
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        text = request.POST.get("text")
        photo = (  # noqa: F841
            request.FILES.get("photo") if "photo" in request.FILES else None
        )
        file = (  # noqa: F841
            request.FILES.get("file") if "file" in request.FILES else None
        )
        home_page_url = request.POST.get("home_page_url")
        parent_comment_id = request.POST.get("reply_id")

        parent_comment = None
        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(
                    comment_id=parent_comment_id
                )  # noqa: E501
            except Comment.DoesNotExist:
                return JsonResponse(
                    {"message": "Parent comment not found"}, status=404
                )  # noqa: E501

        # Create and save the comment
        comment = Comment(
            user_name=user_name,
            email=email,
            text=text,
            home_page_url=home_page_url,
            parent_comment=parent_comment,
        )
        comment.save()
        if photo:
            if not check_image_format(
                photo,
                [
                    "JPG",
                    "JPEG",
                    "GIF",
                    "PNG",
                    "jpg",
                    "jpeg",
                    "gif",
                    "png",
                ],  # noqa: E501
            ):
                return JsonResponse(
                    {"error": "Invalid image format"}, status=405
                )  # noqa: E501

            if not check_image_size(photo, 320, 240):
                photo = scale_image(photo, 320, 240)
            # Upload the processed photo
            photo_url = upload_to_bucket(photo.name, photo, photo.content_type)
            attachment = Attachment(
                comment=comment,
                file_path=photo_url,
                file_type=photo.content_type,
            )
            attachment.save()
        if file:
            if not check_file(file):
                return JsonResponse(
                    {"error": "Invalid file size or format"}, status=405
                )

            # Upload the file
            file_url = upload_to_bucket(file.name, file, file.content_type)
            attachment = Attachment(
                comment=comment,
                file_path=file_url,
                file_type=file.content_type,
            )
            attachment.save()

        try:
            response_data = {
                "message": "Comment added successfully",
                "comment": {
                    "id": comment.comment_id,
                    "user_name": comment.user_name,
                    "text": comment.text,
                    "home_page_url": comment.home_page_url,
                    # Add other relevant fields
                },
            }
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    except jwt.ExpiredSignatureError:
        return HttpResponseForbidden("Token has expired")

    except jwt.InvalidTokenError:
        return HttpResponseForbidden("Invalid token")


@require_http_methods(["POST"])
def like_add(request):
    comment_id = request.POST.get("comment_id")
    user_id = request.session.get(
        "user_id", request.user.id
    )  # Use session user_id for anonymous users

    # Ensure the comment exists
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)

    # Check if the like already exists
    if not Like.objects.filter(comment=comment, user=user_id).exists():
        Like.objects.create(comment=comment, user=user_id)
        updated_like_count = get_new_like_count(comment_id)

        return JsonResponse({"new_like_count": updated_like_count})
    else:
        return JsonResponse({"error": "Like already exists"}, status=400)


@require_http_methods(["POST"])
def like_remove(request):
    comment_id = request.POST.get("comment_id")
    user_id = request.session.get(
        "user_id", request.user.id
    )  # Use session user_id for anonymous users

    # Ensure the comment exists
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)

    # Check if the like exists and delete it
    like = Like.objects.filter(comment=comment, user=user_id).first()
    if like:
        like.delete()
        updated_like_count = get_new_like_count(comment_id)

        return JsonResponse({"new_like_count": updated_like_count})
    else:
        return JsonResponse({"error": "Like not found"}, status=404)


def get_new_like_count(comment_id):
    """Retrieve the updated like count for a specific comment."""
    try:
        comment = Comment.objects.get(comment_id=comment_id)
    except Comment.DoesNotExist:
        return 0  # or handle the error as appropriate

    # Assuming your Like model has a foreign key to Comment
    like_count = Like.objects.filter(comment=comment).count()
    return like_count

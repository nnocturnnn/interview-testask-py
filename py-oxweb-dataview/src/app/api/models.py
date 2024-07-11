from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Company(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

    historical_prices = fields.ReverseRelation["models.HistoricalPrices"]

    class Meta:
        tablename = "companies"

    def __str__(self):
        return self.name


class HistoricalPrices(models.Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    open = fields.DecimalField(max_digits=20, decimal_places=6)
    high = fields.DecimalField(max_digits=20, decimal_places=6)
    low = fields.DecimalField(max_digits=20, decimal_places=6)
    close = fields.DecimalField(max_digits=20, decimal_places=6)
    adj_close = fields.DecimalField(max_digits=20, decimal_places=6)
    volume = fields.IntField()

    company = fields.ForeignKeyField("models.Company", related_name="historical_prices")

    class Meta:
        tablename = "historical_prices"

    def __str__(self):
        return str(self.id)


Company_Pydantic = pydantic_model_creator(Company, name="Companies")
HistoricalPrices_Pydantic = pydantic_model_creator(HistoricalPrices, name="HistoricalPrice")
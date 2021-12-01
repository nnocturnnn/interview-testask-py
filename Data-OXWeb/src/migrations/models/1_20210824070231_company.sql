-- upgrade --
CREATE TABLE IF NOT EXISTS "company" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL
);;
ALTER TABLE "historicalprices" ADD "company_id" INT NOT NULL;
ALTER TABLE "historicalprices" ADD CONSTRAINT "fk_historic_company_c342c9f2" FOREIGN KEY ("company_id") REFERENCES "company" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "historicalprices" DROP CONSTRAINT "fk_historic_company_c342c9f2";
ALTER TABLE "historicalprices" DROP COLUMN "company_id";
DROP TABLE IF EXISTS "company";

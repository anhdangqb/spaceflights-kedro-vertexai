from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
import pyspark.sql.functions as F


# def _is_true(x: pd.Series) -> pd.Series:
#     return x == "t"


# def _parse_percentage(x: pd.Series) -> pd.Series:
#     x = x.str.replace("%", "")
#     x = x.astype(float) / 100
#     return x


# def _parse_money(x: pd.Series) -> pd.Series:
#     x = x.str.replace("$", "").str.replace(",", "")
#     x = x.astype(float)
#     return x


def preprocess_companies(companies: DataFrame) -> DataFrame:
    """Preprocesses the data for companies.

    Args:
        companies: Raw data.
    Returns:
        Preprocessed data, with `company_rating` converted to a float and
        `iata_approved` converted to boolean.
    """
    results = (
        companies
        .withColumn('iata_approved', 
                    F.when(F.col('iata_approved') == 't', True)
                    .otherwise(False))
        .withColumn('company_rating',
                    F.regexp_replace(F.col('company_rating'), '%', '')
                    .cast("double") / 100
                   )
    )
    return results


def preprocess_shuttles(shuttles: DataFrame) -> DataFrame:
    """Preprocesses the data for shuttles.

    Args:
        shuttles: Raw data.
    Returns:
        Preprocessed data, with `price` converted to a float and `d_check_complete`,
        `moon_clearance_complete` converted to boolean.
    """
    results = (
        shuttles
        .withColumn('d_check_complete', 
                    F.when(F.col('d_check_complete') == 't', True)
                    .otherwise(False)
                   )
        .withColumn('moon_clearance_complete',
                    F.when(F.col('moon_clearance_complete') == 't', True)
                    .otherwise(False)
                   )
        .withColumn('price',
                    F.regexp_replace(F.col('price'), '\$', ''))
        .withColumn('price',
                    F.regexp_replace(F.col('price'), ',', '')
                    .cast('double')
                   )
    )
    return results


def create_model_input_table(
    shuttles: DataFrame, companies: DataFrame, reviews: DataFrame
) -> DataFrame:
    """Combines all data to create a model input table.

    Args:
        shuttles: Preprocessed data for shuttles.
        companies: Preprocessed data for companies.
        reviews: Raw data for reviews.
    Returns:
        Model input table.

    """
    rated_shuttles = (
        shuttles
        .join(
            reviews, 
            shuttles.id == reviews.shuttle_id
        )
        .drop('id')
    )
        
    model_input_table = (
        rated_shuttles
        .join(
            companies,
            rated_shuttles.company_id == companies.id
        )
        .drop('id')
        .dropna()
    )
    return model_input_table

import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path

import pandas as pd

# Adjust import path for data functions
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from src.utils.data.data_functions import export_data
from src.config.config_logger import logger


@dataclass
class LPUItem:
    """
    Represents a unit price list (LPU) item with its properties.

    Attributes:
        code (str): Unique identifier for the item
        description (str): Detailed description of the item
        unit (str): Unit of measurement (e.g., m2, un)
        base_price (float): Base price of the item
        category (str): Main category of the item
        subcategory (str): Subcategory of the item
    """

    code: str
    description: str
    unit: str
    base_price: float
    category: str
    subcategory: str


@dataclass
class PricingConfig:
    """
    Configuration for pricing validity and source information.

    Attributes:
        validity_start (str): Start date of price validity (YYYY-MM-DD)
        validity_end (str): End date of price validity (YYYY-MM-DD)
        source (str): Source description of the pricing table
    """

    validity_start: str = "2025-01-01"
    validity_end: str = "2025-10-31"
    source: str = "Tabela Interna v2025.10 – Agência Varejo/Premium (ilustrativa)"


def create_base_items() -> List[LPUItem]:
    """
    Creates a list of base LPU items with predefined values.

    Returns:
        List[LPUItem]: List containing all base LPU items with their properties
    """
    logger.debug("Creating base LPU items")
    items = [
        LPUItem(
            "LPU-001",
            "Piso vinílico em manta, instalação completa",
            "m2",
            97.50,
            "Piso",
            "Vinílico",
        ),
        LPUItem(
            "LPU-002",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-003",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-004",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-005",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-006",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-007",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-008",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-009",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-010",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-011",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-012",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-013",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-014",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-015",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-016",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-017",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-018",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-019",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-020",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-021",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-022",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-023",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-024",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-025",
            "Piso porcelanato PEI 4, assentamento",
            "m2",
            142.00,
            "Piso",
            "Porcelanato",
        ),
        LPUItem(
            "LPU-026",
            "Barra de apoio inox 80 cm para sanitário PCD",
            "un",
            210.00,
            "Acessibilidade",
            "Barra PCD",
        ),
    ]

    return items


def get_regional_factors() -> Dict[str, float]:
    """
    Provides regional price adjustment factors for different states.

    Returns:
        Dict[str, float]: Dictionary mapping state codes to their price factors
        where 1.0 represents the base price (no adjustment)
    """
    return {
        "SP": 1.00,
        "RJ": 1.06,
        "MG": 1.03,
        "PR": 0.98,
        "RS": 1.01,
        "BA": 1.05,
    }


def calculate_regional_price(item: LPUItem, uf: str, factor: float) -> dict:
    """
    Calculates the regional price for an item based on state and factor.

    Args:
        item (LPUItem): The base item to calculate price for
        uf (str): State code (e.g., "SP", "RJ")
        factor (float): Regional price adjustment factor

    Returns:
        dict: Dictionary containing all item information with adjusted price
        and regional metadata
    """
    return {
        "codigo_lpu": item.code,
        "descricao": item.description,
        "unidade": item.unit,
        "preco_lpu": round(item.base_price * factor, 2),
        "uf": uf,
        "categoria": item.category,
        "subcategoria": item.subcategory,
        "validade_inicio": PricingConfig.validity_start,
        "validade_fim": PricingConfig.validity_end,
        "origem": PricingConfig.source,
        "observacoes": f"Preço regional {uf} (fator {factor})",
    }


def generate_price_table() -> pd.DataFrame:
    """
    Generates a complete price table for all items across all regions.

    Returns:
        pd.DataFrame: DataFrame containing all items with their regional prices
        and metadata
    """
    items = create_base_items()
    regional_factors = get_regional_factors()

    price_rows = [
        calculate_regional_price(item, uf, factor)
        for uf, factor in regional_factors.items()
        for item in items
    ]

    return pd.DataFrame(price_rows)


def save_price_table(
    df: pd.DataFrame, filename: str = "lpu_vigente_itau_agencia.csv"
) -> None:
    """
    Saves the price table to a CSV file.

    Args:
        df (pd.DataFrame): Price table to be saved
        filename (str, optional): Output filename. Defaults to "lpu_vigente_itau_agencia.csv"

    Returns:
        None: Prints confirmation message with file name and row count
    """
    export_data(data=df, file_path=filename, create_dirs=True)
    print(f"Gerado: {filename} com {len(df)} linhas.")


def main():
    """
    Main execution function that generates and saves the price table.
    """
    logger.info("Starting LPU price table generation process")
    try:
        price_table = generate_price_table()
        output_file = Path(
            Path(__file__).parents[0], "ks_lpu_vigente_itau_agencias.csv"
        )

        save_price_table(price_table, filename=str(output_file))

        logger.success(
            f"Successfully generated and saved price table with {len(price_table)} rows"
        )
    except Exception as e:
        logger.error(f"Error in price table generation process: {str(e)}")
        raise


if __name__ == "__main__":
    main()

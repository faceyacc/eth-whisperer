from typing import List

import hopsworks
import pandas as pd

from src.feature_store_config import config


# Hopsworks API call to write data to the feature store
def data_to_feature_store(
    feature_group_name: str,
    feature_group_version: int,
    data: List[dict],
    online_or_offline: str,
) -> None:
    """
    Writes data to the Hopsworks feature store

    Args:
        feature_group_name (str): Name of the feature group to write to
        feature_group_version (int): Version of the feature group to write to
        data (List[dict]): Data to write to the feature group

    Returns:
        None
    """
    # Connect to Hopsworks API
    project = hopsworks.login(
        project=config.hopsworks_project_name,
        api_key_value=config.hopsworks_api_key,
    )

    # Get the feature store
    feature_store = project.get_feature_store()  # type: ignore

    # Create a feature group for the OHLC data
    ohlc_feature_group = feature_store.get_or_create_feature_group(
        name=feature_group_name,
        version=feature_group_version,
        description='OHLC data from Kraken',
        primary_key=['product_id', 'timestamp'],
        event_time='timestamp',
        online_enabled=True,
        # stream=True,
    )

    # Transform the data into a DataFrame
    data = pd.DataFrame(data)  # type: ignore

    ohlc_feature_group.insert(
        data,
        write_options= {  # type: ignore
            'start_offline_materialization': True
            if online_or_offline == 'offline' else False
        },
    )

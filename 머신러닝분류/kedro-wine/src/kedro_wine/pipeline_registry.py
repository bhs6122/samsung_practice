from kedro_wine.pipelines import data_processing as dp
from kedro_wine.pipelines import data_science as ds


def register_pipelines():
    prepare = dp.create_pipeline()
    science = ds.create_pipeline()
    return {
        "__default__": prepare + science,
        "data_processing": prepare,
        "data_science": science,
    }

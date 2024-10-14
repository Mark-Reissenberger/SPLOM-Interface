import pandas as pd
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets import load_iris
def data_loader(dataset="iris", target_column = "species") -> pd.DataFrame:
    """
    This function loads the specified dataset and marks the column with the target classes.
    All columns, except the one specified in the target_column argument must be numerical.

    :param dataset: Defaults to the iris dataset from scikit learn. Specify csv path over data_path argument
    :param target_column: name of the column with the classes
    :return: pandas.DataFrame with the target_column being renamed to "classes" and added columns "old_color",
     "new_color", "old_cluster_center" and "new_cluster_center" set to None for all rows
    """

    if dataset == "iris":
        iris_bunch = load_iris()
        df = pd.DataFrame(iris_bunch.data, columns=iris_bunch.feature_names)
        df["classes"] = iris_bunch.target
        df["old_color"] = None
        df["new_color"] = None
        df["old_cluster_center"] = None
        df["new_cluster_center"] = None
        return df
    else:
        df = pd.read_csv(dataset)
        df["classes"] = df[target_column]
        df["old_color"] = None
        df["new_color"] = None
        df["old_cluster_center"] = None
        df["new_cluster_center"] = None
        return df


def data_transformer(df, x, y, color_map="hsv", clustering_algorithm="mean_shift", **kwargs) -> pd.DataFrame:
    """
    This function transforms a dataframe in the specified way. This function can take a new dataframe or an old one
    where certain parameters should be changed

    :param df: pandas
    :param x: x-axis name as a basis for clustering
    :param y: y-axis name as a basis for clustering
    :param color_map: matplotlib color map name to be applied, defaults to "hsv" color map
    :param clustering_algorithm: clustering algorithm to apply to the data, defaults to "mean_shift"
    :return: transformed dataframe
    """
    bandwith = kwargs.get("bandwith", None)

    if bandwith is None:
        X = df.drop(columns=["classes", "old_color", "new_color"])
        bandwidth = estimate_bandwidth(X, quantile=0.2)

    mean_shift = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    mean_shift.fit(X)
    df["old_cluster_center"] = df["new_cluster_center"]
    df["new_cluster_center"] = mean_shift.cluster_centers_


def color_for_cluster(df, color_map, x, y, old_clusters=False, **kwargs):
    """
    Creates color codes for each point, according to its cluster center and old cluster center if applicable.

    :param df: dataframe with old and new cluster centers and colors per point. These can be set to None if less than
    two iterations have passed
    :param color_map: color map to use when
    :param x: x-axis
    :param y: y-axis
    :param old_clusters:
    :return:
    """
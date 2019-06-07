from visualization.visualize import Visualizer
from data.make_dataset import DataTransform

def main():
    vis = Visualizer("../data/raw/train.csv","../data/raw/item_metadata.csv")
    data = DataTransform(train=vis.get_train_data(), metadata=vis.get_metadata())
    data.transform_categorical_to_discret("action_type")
    vis.count_column("action_type")
    #vis.column_distribution("action_type",False)


if __name__ == "__main__":
    main()

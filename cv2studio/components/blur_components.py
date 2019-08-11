import pickle


class ComponentState(dict):
    def load(self, path: str):
        """
        Loads a component state from a drive
        :param path: path to a pickle file where a component is stored
        :return: None
        """
        with open(path, 'br') as f:
            self = ComponentState(pickle.load(f))

    def save(self, path: str):
        """
        Saves a component
        :param path: path where to save a component
        :return: None
        """
        with open(path, 'bw') as f:
            pickle.dump(self, f)

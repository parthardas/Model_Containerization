import pickle
from abc import ABC, abstractmethod

class SklearnModel(ABC):
    """
    Abstract Base Class for sklearn models
    """
    def __init__(self, model=None):
        self.model = model
        self.scaler = None
        self.le = None

    def load_model_from_pkl(self, filepath):
        with open(filepath, 'rb') as file:
            self.model = pickle.load(file)
    
    def load_scaler_from_pkl(self, filepath):
        with open(filepath, 'rb') as file:
            self.scaler = pickle.load(file)
    
    def load_le_from_pkl(self, filepath):
        with open(filepath, 'rb') as file:
            self.le = pickle.load(file)

    @abstractmethod
    def preprocess(self, data):
        pass

    @abstractmethod
    def predict(self, data):
        pass

    @abstractmethod
    def preprocess(self, data):
        pass

    def infer(self, data):
        preprocessed_data = self.preprocess(data)
        predictions = self.predict(preprocessed_data)
        return self.post_process(predictions)


class KnnClassifier(SklearnModel):
    def __init__(self, model=None, model_path=None, scaler_path=None, le_path=None):
        super().__init__(model)
        if model_path:
            self.load_model_from_pkl(model_path)
        if scaler_path:
            self.load_scaler_from_pkl(scaler_path)
        if le_path:
            self.load_le_from_pkl(le_path)
        
    def preprocess(self, data):
        if self.scaler:
            data = self.scaler.transform(data)
        return data

    def predict(self, data):
        preprocessed_data = self.preprocess(data)
        if not self.model:
            raise Exception("Model not found. Please train the model first.")
        predictions = self.model.predict(preprocessed_data)
        return self.post_process(predictions)

    def post_process(self, output):
        if self.le:
            return self.le.inverse_transform(output)
        return output

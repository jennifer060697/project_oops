from sentence_transformers import SentenceTransformer
from keras.models import Sequential, load_model
import pandas as pd
from tensorflow_addons.metrics import F1Score


s_bert = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

class CombinedModel(Sequential):
    def __init__(self, s_bert, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s_bert = s_bert
        self.model = model

    def predict(self, input):
        vector = self.s_bert.encode(input)
        vector = pd.DataFrame(vector).T
        return self.model.predict(vector)[0].tolist()

sequential_model = load_model('sequential_model')

combined_model = CombinedModel(s_bert, sequential_model)

# Use the model for prediction
# input_data = '가성비 있는 맛집' # Input data to be fed into the model
# predictions = combined_model.predict(input_data)

# print(predictions)

# 확률
# targets = ['가성비',
#  '귀여운',
#  '넓은',
#  '단체',
#  '만족',
#  '모던',
#  '분위기',
#  '비주얼',
#  '아늑',
#  '위생',
#  '응대',
#  '이색음식',
#  '이색테마',
#  '클래식',
#  '혼자']
# df_result = pd.DataFrame()
# df_result.index = targets
# df_result['점수'] = predictions
# print(df_result)

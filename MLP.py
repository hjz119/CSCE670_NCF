from keras.models import Model
from keras.layers import Dense, Input,concatenate, Flatten, Embedding
import numpy as np
import ncf_helper as helper

num_predictive_factors = 8

batch_size = 1

# embedding size is 2 * num_predictive_factors if MLP is 3 layered

interaction_mx = np.load('input/int_mat.npy')
# load data
inputs, labels = helper.training_data_generation('input/one_training_data',interaction_mx, 5)

#https://datascience.stackexchange.com/questions/13428/what-is-the-significance-of-model-merging-in-keras
user_input = Input(shape=(1,),name='user_input')
#item_input = Input(shape=(len(one_hot_movies),),name='item_input')
item_input = Input(shape=(1,),name='item_input')
user_embed = Flatten()(Embedding(len(inputs['user_input']) + 1, num_predictive_factors * 2, input_length=1)(user_input))
item_embed = Flatten()(Embedding(len(inputs['item_input']) + 1, num_predictive_factors * 2, input_length=1)(item_input))
merged_embed = concatenate([user_embed, item_embed], axis=1)
mlp_1 = Dense(32, activation='relu', name='mlp_1')(merged_embed)
mlp_2 = Dense(16, activation='relu', name='mlp_2')(mlp_1)
mlp_3 = Dense(8, activation='relu', name='mlp_3')(mlp_2)
main_output = Dense(1, activation='sigmoid',name='main_output')(mlp_3)

model = Model(inputs=[user_input, item_input], output=main_output)
model.compile(optimizer='Adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(inputs, labels, batch_size = 64, epochs = 10)

#Save weights for full_model
#Save weights for full_model
wmlp1= model.get_layer('mlp_1').get_weights()
np.save('MLP_WE/mlp_1_weights_array0', wmlp1[0])
np.save('MLP_WE/mlp_1_weights_array1', wmlp1[1])
np.save('MLP_WE/mlp_2_weights',model.get_layer('mlp_2').get_weights());
np.save('MLP_WE/mlp_3_weights',model.get_layer('mlp_3').get_weights());
np.save('MLP_WE/mlp_user_embed_weights',model.get_layer('MLP_user_embed').get_weights());
np.save('MLP_WE/mlp_item_embed_weights',model.get_layer('MLP_item_embed').get_weights());


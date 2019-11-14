import tensorflow as tf
import os
from bilm import TokenBatcher, BidirectionalLanguageModel, dump_token_embeddings, weight_layers
from sklearn.metrics.pairwise import cosine_similarity

vocab_file = 'vocabulary.txt'
options_file = 'output/checkpoints/options.json'
weight_file = 'output/weights.hdf5'

# Dump token embeddings to a file
token_embedding_file = 'output/elmo_token_embeddings.hdf5'
dump_token_embeddings(vocab_file, options_file, weight_file, token_embedding_file)
tf.reset_default_graph()

# Inference
batcher = TokenBatcher(vocab_file)
player_deck = '01NX015 01NX040 01NX040 01NX040 01NX035 01NX035 01NX012 01NX012 01NX012 01NX043 01NX043 01NX043 01NX016 01NX016 01NX016 01NX007 01NX007 01NX007 01NX037 01NX037 01NX037 01NX020 01NX020 01NX020 01NX039 01NX039 01NX039 01NX022 01NX004 01NX004 01NX021 01NX021 01NX021 01NX019 01NX019 01NX008 01NX008 01NX009 01NX009 01NX009'
possible_deck1 = '01NX015 01NX040 01NX040 01NX040 01NX035 01NX035 01NX012 01NX012 01NX012 01NX043 01NX043 01NX043 01NX016 01NX016 01NX016 01NX007 01NX007 01NX007 01NX037 01NX037 01NX037 01NX020 01NX020 01NX020 01NX039 01NX039 01NX039 01NX022 01NX004 01NX004 01NX021 01NX021 01NX021 01NX019 01NX019 01NX008 01NX008 01NX014 01NX014 01NX014'
possible_deck2 = '01NX015 01NX040 01NX040 01NX040 01NX035 01NX035 01NX012 01NX012 01NX012 01NX043 01NX043 01NX043 01NX016 01NX016 01NX016 01NX007 01NX007 01NX007 01NX037 01NX037 01NX037 01NX020 01NX020 01NX020 01NX039 01NX039 01NX039 01NX022 01NX004 01NX004 01NX021 01NX021 01NX021 01NX019 01NX019 01NX008 01NX008 01FR019 01FR019 01FR019'
tokenized_player_deck = player_deck.split()
tokenized_possible1 = possible_deck1.split()
tokenized_possible2 = possible_deck2.split()
bilm = BidirectionalLanguageModel(
    options_file, 
    weight_file,
    use_character_inputs=False,
    embedding_weight_file=token_embedding_file
)
deck_token_ids = tf.placeholder('int32', shape=(None, None))
possible1_token_ids = tf.placeholder('int32', shape=(None, None))
possible2_token_ids = tf.placeholder('int32', shape=(None, None))
deck_embeddings_op = bilm(deck_token_ids)
possible1_embeddings_op = bilm(possible1_token_ids)
possible2_embeddings_op = bilm(possible2_token_ids)

elmo_deck_input = weight_layers('input', deck_embeddings_op, l2_coef=0.0)
with tf.variable_scope('', reuse=True):
    elmo_p1_input = weight_layers('input', possible1_embeddings_op, l2_coef=0.0)
    elmo_p2_input = weight_layers('input', possible2_embeddings_op, l2_coef=0.0)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    deck_ids = batcher.batch_sentences(tokenized_player_deck)
    p1_ids = batcher.batch_sentences(tokenized_possible1)
    p2_ids = batcher.batch_sentences(tokenized_possible2)

    deck_, p1_, p2_ = sess.run(
        [elmo_deck_input['weighted_op'], elmo_p1_input['weighted_op'], elmo_p2_input['weighted_op']], 
        feed_dict={deck_token_ids: deck_ids, possible1_token_ids: p1_ids, possible2_token_ids: p2_ids}
    )
    
    print(len(deck_[0]))
    # print(cosine_similarity(deck_[0][39], p1_[0][39]))
    # print(cosine_similarity(deck_[0][39], p2_[0][39]))
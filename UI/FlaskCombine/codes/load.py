from gensim.models.keyedvectors import KeyedVectors

def main():
    model_path = '/home/shriniwas/BE/BEProj/UI/Flask/input/GoogleNews-vectors-negative300.bin'
    w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    return w2v_model

from vectordb.base_db import BaseVectorStore


def test_base_vector_store_is_abstract():
    try:
        BaseVectorStore()
        assert False, "BaseVectorStore should not be instantiable"
    except TypeError:
        pass
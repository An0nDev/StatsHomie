from typing import List

class DictCompressor:
    @staticmethod
    def compress (*, decompressed : dict, _format : List [str]):
        compressed = []
        for field in _format:
            compressed.append (decompressed.get (field, None))
        return compressed
    @staticmethod
    def decompress (*, compressed : list, _format : List [str]):
        decompressed = {}
        index = 0
        for field in _format:
            decompressed [field] = compressed [index]
            index += 1
        return decompressed
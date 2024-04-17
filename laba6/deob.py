import zlib, base64

def decode_decompress(data):
    try:
        # Поправка padding для Base64
        padding = len(data) % 4
        if padding != 0:
            data += '=' * (4 - padding)

        # Декодирование Base64
        decoded_data = base64.b64decode(data)

        # Попытка декомпрессии с использованием zlib
        try:
            decompressed_data = zlib.decompress(decoded_data).decode('utf-8')
            return decompressed_data
        except zlib.error as e:
            print("zlib decompression error:", e)
            # В случае ошибки декомпрессии попробуем вернуть декодированные данные
            # Это может быть полезно, если данные не были сжаты
            return decoded_data.decode('utf-8')

    except (base64.binascii.Error, UnicodeDecodeError) as e:
        print("Base64 decoding error or UTF-8 decode error:", e)
        return None

def recursive_decode(data, max_depth=10):
    current_depth = 0
    while current_depth < max_depth:
        result = decode_decompress(data)
        if result is None:
            print("Decoding failed at depth:", current_depth)
            break
        print("Decoding successful at depth:", current_depth)
        if "exec(" in result and "base64.b64decode(" in result:
            try:
                next_data_start = result.index("base64.b64decode('") + 19
                next_data_end = result.index("')", next_data_start)
                data = result[next_data_start:next_data_end]
            except ValueError:
                print("No more encoded data found at depth:", current_depth)
                return result
        else:
            return result
        current_depth += 1
    return result

encoded_string = "eJwkmsdyg2y2Ref9FD3..."
final_output = recursive_decode(encoded_string)
print("Final output:", final_output)

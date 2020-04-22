from SharedUtils.DBUtils.db_api_parsed_conv import ParsedConversationsAPI
from SharedUtils.DBUtils.db_api_schemas import SchemasAPI
from SharedUtils.DBUtils.db_api_raw_conv import RawConversationsAPI
from SharedUtils.raw_conversation import RawConversation


def main():
    print("\n\n\nRaw\n")
    raw = RawConversationsAPI('shise.db')
    raw.reset()
    raw.save_one_conversation(RawConversation('url1', 'GET', 'lulul', 'lalala', 'lala', 'lulul'))
    raw.save_one_conversation(RawConversation('url2', 'lala', 'lulul', 'lalala', 'lala', 'lulul'))
    # Raw.save_all_conversations()
    print(raw.get_all_conversations()[0].method)
    raw.delete_one_conversation(1)
    raw.delete_all_conversations()
    raw.__delete__(None)

    print("\n\n-----------------------------------\n")

    print("Parsed\n")
    parsed = ParsedConversationsAPI('shise.db')
    parsed.reset()
    parsed.save_conversation_by_api('api1', 'GET', 'conv1')
    parsed.save_conversation_by_api('api1', 'SET', 'conv2')
    parsed.save_conversation_by_api('api2', 'SET', 'conv3')
    print(parsed.get_list_apis())
    print(parsed.get_conversations_for_api('api2', 'SET'))
    print(parsed.get_method_for_api('api1'))
    parsed.delete_conversations_for_api('lalala', 'lala')
    parsed.__delete__(None)

    print("\n\n-----------------------------------\n")

    print("Schamas\n")

    schemas = SchemasAPI('shise.db')
    schemas.reset()
    schemas.save_schema('lalala', 'GET', 'lili979li')
    schemas.save_schema('lalalg', 'SET', 'lili97guogo9li')
    schemas.save_schema('lalalg', 'GET', 'lili979lvdsvcwvwi')
    print(schemas.get_schema_for_api('lalala', 'GET'))
    print(schemas.get_all_schemas())
    schemas.delete_schema_for_api('lalala', 'lala')
    schemas.delete_all_schemas()
    schemas.__delete__(None)
    print("ales iz zeyer gut\n")


main()

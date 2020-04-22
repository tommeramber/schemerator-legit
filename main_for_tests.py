from SharedUtils.DBUtils.db_api_parsed_conv import ParsedConversationsAPI
from SharedUtils.DBUtils.db_api_schemas import SchemasAPI
from SharedUtils.DBUtils.db_api_raw_conv import RawConversationsAPI
from SharedUtils.raw_conversation import RawConversation


def main():
    print("\n\n\nRaw\n")
    Raw = RawConversationsAPI('shise.db')
    Raw.reset()
    Raw.save_one_conversation(RawConversation('url1', 'lala', 'lulul', 'lalala', 'lala', 'lulul'))
    Raw.save_one_conversation(RawConversation('url2', 'lala', 'lulul', 'lalala', 'lala', 'lulul'))
    # Raw.save_all_conversations()
    Raw.get_all_conversations()
    Raw.delete_one_conversation(1)
    Raw.delete_all_conversations()
    Raw.__delete__(None)

    print("\n\n-----------------------------------\n")

    print("Parsed\n")
    parsed = ParsedConversationsAPI('shise.db')
    parsed.reset()
    parsed.save_conversation_by_api('api1', 'GET', 'conv1')
    parsed.save_conversation_by_api('api1', 'SET', 'conv2')
    parsed.save_conversation_by_api('api2', 'SET', 'conv3')
    parsed.get_list_apis()
    parsed.get_conversations_for_api('api2', 'SET')
    parsed.get_method_for_api('api1')
    parsed.delete_conversations_for_api('lalala', 'lala')
    parsed.__delete__(None)

    print("\n\n-----------------------------------\n")

    print("Schamas\n")

    Schemas = SchemasAPI('shise.db')
    Schemas.reset()
    Schemas.save_schema('lalala', 'GET', 'lili979li')
    Schemas.save_schema('lalalg', 'SET', 'lili97guogo9li')
    Schemas.save_schema('lalalg', 'GET', 'lili979lvdsvcwvwi')
    #Schemas.get_schema_for_api('lalala', 'GET')
    #Schemas.get_all_schemas()
    Schemas.delete_schema_for_api('lalala', 'lala')
    Schemas.delete_all_schemas()
    Schemas.__delete__(None)
    print("ales iz zeyer gut\n")


main()

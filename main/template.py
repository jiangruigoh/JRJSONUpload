@api_view(['GET'])
def PoSupplierCopy(request, search_refno):
    print(search_refno)

    querystr = """


    """
   
    result = panda.raw_query(querystr,[search_refno,search_refno,search_refno,search_refno])
    result={"query1":result}

    # querystr="""
    
    # """
    # result2=panda.raw_query(querystr,[search_refno])    
    # result["query2"] = result2

    # querystr="""
    
    # """
    # result3=panda.raw_query(querystr,[search_refno,search_refno,search_refno,search_refno])    
    # result["query3"] = result3

    # querystr="""
    
    # """

    # result4=panda.raw_query(querystr,[search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno,search_refno])    
    # result["query4"] = result4
    return Response(result, status=status.HTTP_200_OK)   


    
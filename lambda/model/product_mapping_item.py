class ProductMappingItem:
    
    def __init__(self, competitorCatalogId, abCatalogId, reason, webPageLink):
        self.competitorCatalogId = competitorCatalogId
        self.abCatalogId = abCatalogId
        self.reason = reason
        self.webPageLink = webPageLink
    
    def getCompetitorCatalogId():
        return self.competitorCatalogId
        
    def getAbCatalogId():
        return self.abCatalogId
        
    def getReason():
        return self.reason
        
    def getWebPageLink():
        return self.webPageLink
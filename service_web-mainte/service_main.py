class ServiceMain():
    
    def mapping(self,dto,dao):
        return [ dto(*record) for record in dao ]

    def isnamedtupleinstance(self,x):
        _type = type(x)
        bases = _type.__bases__
        if len(bases) != 1 or bases[0] != tuple:
            return False
        fields = getattr(_type, '_fields', None)
        if not isinstance(fields, tuple):
            return False
        return all(type(i)==str for i in fields)

    def unpack(self,obj):
        if isinstance(obj, dict):
            return {key: self.unpack(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.unpack(value) for value in obj]
        elif self.isnamedtupleinstance(obj):
            return {key: self.unpack(value) for key, value in obj._asdict().items()}
        elif isinstance(obj, tuple):
            return tuple(self.unpack(value) for value in obj)
        else:
            return obj
    


from pydantic import BaseModel, RootModel


class PydanticBase(BaseModel):
    pass


class PydanticRootBase(RootModel):
    root: list[PydanticBase]

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    def __iter__(self):
        return iter(self.root)

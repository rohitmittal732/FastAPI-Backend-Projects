from pydantic import BaseModel,Field
from typing import Annotated,List,Optional,Dict

class Patients(BaseModel):
    name:str
    address:str
    mobile_no: Annotated[str,Field(default=None,min_length=10,max_length=10)]
    contact_info:Dict[str,str]
    married:bool=False
    weight:float

patient_info={"name":"nitish","address":"bihar","mobile_no":"1234567899","contact_info":{"email":"rwohs","info":"haryana"},
                  "weight":34}
    
def get_patient(patient:Patients):
    print(patient.name)
    print(patient.address)
    print(patient.weight)
    
patient1=Patients(**patient_info)

get_patient(patient1)


#here we learn type validation from pydantic firstly make class in which take BaseModel as inherit in which basemodel checks type validataion
#by own and give errors also and here the class we make for ideal schema in which we tells the following parameter of this type and also use constraint 
# for validation like max_length,default then we make rough schema using the parameters as define then we make function in which we make object for class
# then declare our woek and now we make dataframe in which data store and using class name we pass the unpacked dictionary rough schema then we call function 
# and print the data
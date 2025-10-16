from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pathlib import Path
from typing import List
from ..database import get_db
from ..models import User
#from ..sunspecmodels import UserModel
from ..schemas import UserCreate, UserOut, UserUpdate
from ..sunspecshemas import SunspecReturnData,SunspecRequestDataOpenAdr
from ..deps import get_current_user,oauth2_scheme
from ..security import decode_token
import sunspec2.modbus.client as client
from sunspec2.file.client import FileClientDevice
from pprint import pprint


router = APIRouter(prefix="/sunspec", tags=["sunspec"])

@router.post("/updatesunspecdevice", response_model=SunspecReturnData, status_code=status.HTTP_200_OK)
def update_sunspecDevice(payload: SunspecRequestDataOpenAdr, db: Session = Depends(get_db)):
    print("payload===",payload)
    json_path = (Path(__file__).resolve().parents[2] / "model_702_data.json")
    print("json_path===",json_path)
    try:
        d = FileClientDevice(str(json_path))
        d.scan()  # safe with file client; enumerates models
        
        #pprint({k: [list(m.points.keys()) for m in v] for k, v in d.models.items()})

        print("models keys:", list(d.models.keys()))
        common_list = d.models.get(1) or d.models.get("common")
        common = common_list[0]
        print("Common model points:")
        for name, pt in common.points.items():
          print(f"  {name} = {pt.value}")
        
        print("SN:", common.points["SN"].value)
        common.points["SN"].value = "CERO-3333333"
        common.points["SN"].write() 

        m702_list = d.models.get(702) or d.models.get("DERCapacity")
        m702 = m702_list[0]
        for name in ("WMaxRtg", "VNomRtg", "CtrlModes"):
            if name in m702.points:
                print(f"{name} = {m702.points[name].value}")

       
        #print("models==",d.models.SN)
        #m702 = d.models[702]
        #print("WMaxRtg (W):", m702.points["WMaxRtg"].value)
        #print("CtrlModes bitfield:", m702.points["CtrlModes"].value)

    except FileNotFoundError:
        raise HTTPException(
            status_code=500, 
            detail=f"model_702_data.json not found at: {json_path}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SunSpec load error: {e}")


    #d = FileClientDevice("model_702_data.json")
    #print(d)
    #m702 = d.models[702]
    #print("WMaxRtg (W):", m702.points["WMaxRtg"].value)
    #print("CtrlModes bitfield:", m702.points["CtrlModes"].value)
    #common (model 1), DERVoltVar (model 705)
    #d = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
    #d.scan()
    #devicemodels = d.models
    #Get the value on the point "Ena" in the "DERVoltVar" model:
    #print(d.DERVoltVar[0].Ena.value)
    #Set the value for the point and write to the device:
    #d.DERVoltVar[0].Ena.value = 1
    #d.DERVoltVar[0].write()
    #print(d.DERVoltVar[0].read())

    return SunspecReturnData(data=payload)

import { useState } from "react";
import "./App.css";
import Stars from "./Stars";
import Uplaod from "./Upload";


const App = () => {
  const [displayResults, setDisplayResults] = useState(false);
  const [showUploaded, setShowUploaded] = useState(false);
  const[imgSrc1,setImgSrc1]= useState("https://cdn.pixabay.com/photo/2023/11/24/20/17/bosnia-8410601_1280.jpg");
  const[imgSrc2,setImgSrc2]= useState("https://cdn.pixabay.com/photo/2023/11/24/20/17/bosnia-8410601_1280.jpg");
  const [name,setName] = useState("Brock Lesnar")
  const handleUploadMsg = () => {
    
    setShowUploaded(true);
  }

  const handleSubmit = async() => {
    // console.log(data);
    
    const formData = new FormData();
    formData.append("file",data);
    const formData2 = new FormData();
    const response = await fetch("http://localhost:5000/getClass",{
      method:"POST",
      body:formData
      
    })
    const responseData = await response.json();
    formData2.append("filename",responseData.count);
    
    const res = await fetch("http://localhost:5000/get_processed_image",{
      method:"POST",
      body:formData2
      
    })
    const resData = await res.blob();
    const imageUrl = URL.createObjectURL(resData);
    console.log("resData: ",res);
    setDisplayResults(true);
    console.log(data);
    setImgSrc1(URL.createObjectURL(data));
    setImgSrc2(imageUrl);
    console.log("responseData: ",responseData);
    setData(responseData.class);
  }

  const [data, setData] = useState({});

  return (
    <>
      <Stars />
      <section>
        <h1>Ear Recognition</h1>
        {!displayResults && (
          <>
            <Uplaod  onChange={handleUploadMsg} setFile={setData}/>
            {showUploaded && <h2 className="text-class">Uploaded</h2>}
            {/* <h2 className="text-class">Test</h2> */}
            <button onClick={handleSubmit}>Submit</button>
          </>
        )}
        {
          displayResults && <>
          <div className="img">
            <img src={imgSrc1||"https://cdn.pixabay.com/photo/2023/11/24/20/17/bosnia-8410601_1280.jpg"} />
            <img src={imgSrc2||"https://cdn.pixabay.com/photo/2023/11/24/20/17/bosnia-8410601_1280.jpg"} />
          </div>
          <h1 style={{fontSize:"2rem"}}>The name of the person predicted is: {data||"John Doe"}</h1>
          <button onClick={() => {setDisplayResults(false);setShowUploaded(false)}}>Upload Another One!</button>
          </>
        }
      </section>
    </>
  );
};
export default App;

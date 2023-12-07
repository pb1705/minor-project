import "./Upload.css";
import UploadIcon from "./upload.png";
const Uplaod = (props) => {
  const handleChange=(e)=>{
    props.onChange(e);
    // console.log(e.target.files[0])
    props.setFile(e.target.files[0]);
  }
  return (
    <div className="outerContainer">
      <div className="innerContainer">
        <form>
          <label for="file">
            <img src={UploadIcon}></img>
            <p>Click to upload your files</p>
            <p>Supported formats: SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
          </label>
          <input type="file" id="file" multiple onChange={handleChange}/>
          {/* <button onClick={handleChange}>ABC</button> */}
        </form>
      </div>
      
    </div>
  );
};
export default Uplaod;

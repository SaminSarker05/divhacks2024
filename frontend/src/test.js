import React, { useState } from 'react';
import axios from 'axios';

function Test() {
   // new line start
   const [profileData, setProfileData] = useState(null)

   function getData() {
     axios({
       method: "GET",
       url:"http://127.0.0.1:5000/home",
     })
     .then((response) => {
       const res =response.data
       setProfileData(({
         profile_name: res.name,
         about_me: res.about}))
     }).catch((error) => {
       if (error.response) {
         console.log(error.response)
         console.log(error.response.status)
         console.log(error.response.headers)
         }
     })}
     //end of new line 
 
   return (
     <div className="App">
       <header className="App-header">
 
         <p>To get your profile details: </p>
         <button onClick={getData}>Click me</button>
         {profileData && <div>
               <p>Profile name: {profileData.profile_name}</p>
               <p>About me: {profileData.about_me}</p>
             </div>
         }
       </header>
     </div>
   );
}

export default Test;

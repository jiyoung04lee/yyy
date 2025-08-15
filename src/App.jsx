import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppFrame from './components/AppFrame.jsx';
import PhoneSheet from './scrollPage/Scroll_sheet.jsx';
import Profile from './mypage_profile/MyProfile.jsx';
import Header from './components/Header.jsx';
import NavBar from './components/NavBar.jsx';

export default function App() {
  return (
    <AppFrame>
      <div className="phone-stage">
        <Header/>
        <PhoneSheet />
        {/* <Profile/> */}
        {/* <NavBar/> */}
      </div>
    </AppFrame>
  );
}
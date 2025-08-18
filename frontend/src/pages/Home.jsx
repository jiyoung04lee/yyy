import { Link } from "react-router-dom";
import { useState } from "react";
import Header from '../components/Header';
import NavBar from '../components/NavBar';
import Party from '../assets/party.jpg';
import Date from '../assets/date.svg';
import Check from '../assets/check.svg';
import Apply from '../assets/apply.svg';
import Location from '../assets/location.svg';
import PopupImg from '../assets/bell.svg';
import './home.css';

export default function Home() {
  // 테스트용 임시 데이터 2개
  const [partyList, setPartyList] = useState([
    {
      id: 1,
      image: Party,
      name: "#유학생과_언어교류",
      date: "08.25. 18:00",
      person: "12/20",
      location: "주당끼리",
    },
    {
      id: 2,
      image: Date,
      name: "#주말_보드게임",
      date: "08.26. 15:00",
      person: "8/10",
      location: "홍대입구",
    },
  ]);
  const [showPopup, setShowPopup] = useState(false);

  return (
    <>
      <Header />
      <div className='title'>OO님께 추천하는 파티🥳</div>

      {partyList.map((party) => (
        <div className="party-block" key={party.id}>
          <Link to="/notifications" aria-label="알림">
            <div className="party-img-wrap">
              <img src={party.image} alt="" className="party-img" draggable="false" />
              <div className="party-badge">
                <img src={Location} alt="위치 아이콘" />
                <span>{party.location}</span>
              </div>
            </div>
          </Link>

          <div className='partyName'>{party.name}</div>
          <div className='date'>
            <img src={Date} alt="" />
            <span className="dateText">{party.date}</span>
          </div>
          <div className='person'>
            <img src={Check} alt="" />
            <span className="dateText">{party.person}</span>
          </div>

          <button
            className="apply-btn"
            onClick={() => setShowPopup(true)}
            aria-label="팝업 띄우기"
          >
            <img src={Apply} alt="버튼" />
          </button>
          
          {showPopup && (
            <div className="popup-overtlay" onClick={() => setShowPopup(false)}>
              <img src={PopupImg} al="팝업" className="popup-img" />
            </div>
          )}
        </div>
      ))}
      <div className='spaceExpansion'></div>
      <NavBar />
    </>
  );
}
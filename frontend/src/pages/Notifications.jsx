import { useNavigate } from 'react-router-dom';
import Back from '../assets/left_black.svg';
import './notifications.css';

export default function Notifications() {
  const navigate = useNavigate();

  return (
    <>
      <div className="notifications-header">
        <button
          onClick={() => navigate(-1)}
          className="back-button"
          aria-label="뒤로가기"
        >
          <img src={Back} alt="뒤로가기 아이콘" className="back-icon" />
        </button>
        <span className="notifications-title">알림</span>
      </div>

      <div className="notification-block">
        <div className="notifications-content">
          <div>신청하신 ‘#금요일_저녁_칵테일파티’가 곧 열릴 예정이에요. 파티 즐길 준비 됐나요?</div>
        </div>
        <div className="notifications-day">
          <div>5일 전</div>
        </div>
        <div className="notification-divider"></div>
      </div>

      <div className="notification-block">
        <div className="notifications-content">
          <div>신청하신 ‘#금요일_저녁_칵테일파티’가 곧 열릴 예정이에요. 파티 즐길 준비 됐나요?</div>
        </div>
        <div className="notifications-day">
          <div>5일 전</div>
        </div>
        <div className="notification-divider"></div>
      </div>

      <div className='spaceExpansion'></div>
    </>
  );
}

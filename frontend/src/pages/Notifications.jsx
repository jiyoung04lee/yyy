import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Back from '../assets/left_black.svg';
import './notifications.css';

export default function Notifications() {
  const navigate = useNavigate();
  const [notices, setNotices] = useState([]);
  const [showLoginPopup, setShowLoginPopup] = useState(false);

  useEffect(() => {
    const fetchNotices = async () => {
      try {
        const token = localStorage.getItem("access");
        if (!token) {
          setShowLoginPopup(true);
          return;
        }

        const response = await fetch(
          "http://127.0.0.1:8000/api/notice/upcoming/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.status === 401) {
          setShowLoginPopup(true);
          return;
        }

        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();
        setNotices(data);
      } catch (error) {
        console.error("알림 데이터를 불러오는 중 오류 발생:", error);
        setShowLoginPopup(true);
      }
    };

    fetchNotices();
  }, []);

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

      {/* 로그인 안내 팝업 */}
      {showLoginPopup && (
        <div className="popup-overlay">
          <div className="popup-box">
            <p>파티 알림은 로그인 후 확인하실 수 있습니다.</p>
            <div className="popup-actions">
              <button
                className="login-btn"
                onClick={() => navigate("/kakao-login")}
              >
                로그인하기
              </button>
              <button
                className="back-btn"
                onClick={() => navigate("/")}
              >
                뒤로가기
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 알림 목록 */}
      {!showLoginPopup &&
        (notices.length === 0 ? (
          <div className="notification-empty">새 알림이 없습니다.</div>
        ) : (
          notices.map((notice) => (
            <div key={notice.party_id} className="notification-block">
              <div className="notifications-content">
                <div>{notice.message}</div>
              </div>
              <div className="notifications-day">
                <div>
                  {new Date(notice.start_time).toLocaleString("ko-KR", {
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              </div>
              <div className="notification-divider"></div>
            </div>
          ))
        ))}

      <div className="spaceExpansion"></div>
    </>
  );
}

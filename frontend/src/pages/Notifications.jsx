import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Back from 'src/assets/left_black.svg';
import './notifications.css';

export default function Notifications() {
  const navigate = useNavigate();
  const [notices, setNotices] = useState([]);

    useEffect(() => {
    const fetchNotices = async () => {
      try {
        // upcoming 엔드포인트에서 알림 가져오기
        const response = await fetch("http://127.0.0.1:8000/api/notice/upcoming/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`, // JWT 토큰
          },
        });
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        const data = await response.json();
        setNotices(data);
      } catch (error) {
        console.error("알림 데이터를 불러오는 중 오류 발생:", error);
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

      {notices.length === 0 ? (
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
      )}

      <div className="spaceExpansion"></div>
    </>
  );
}

import './PartySmall.css';

export default function PartySmall(props) {
  // 더 직관적인 prop 이름(기존 이름과 매핑해 하위호환 유지)
  const {
    eventTitle    = props.title,
    eventDate     = props.date,
    placeName     = props.location,
    placeImageUrl = props.thumbnailUrl,
    attendees     = props.current ?? 0,
    capacity      = props.capacity ?? 0,
    onClickDetail = props.onClick,
  } = props;

  const d = new Date(eventDate);
  const fmt =
    `${String(d.getMonth()+1).padStart(2,'0')}.${String(d.getDate()).padStart(2,'0')}. ` +
    `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;

  return (
    <article className="party-item">
      <div className="party-item__image">
        <img src={placeImageUrl} alt={eventTitle} />
        {placeName && <span className="party-item__place-badge">📍 {placeName}</span>}
      </div>

      <div className="party-item__content">
        <h3 className="party-item__title">{eventTitle}</h3>

        <div className="party-item__meta">
          <span className="party-item__meta-icon" aria-hidden>🗓️</span>
          <span>{fmt}</span>
        </div>

        <div className="party-item__meta">
          <span className="party-item__meta-icon" aria-hidden>✅</span>
          <span>{attendees}/{capacity}</span>
        </div>

        <button className="party-item__button" onClick={onClickDetail}>상세보기</button>
      </div>
    </article>
  );
}

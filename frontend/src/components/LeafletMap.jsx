import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// 백엔드에서 제공하는 지도 이미지 경로
const mapImageUrl = 'http://127.0.0.1:8000/static/map.png';
// 지도 이미지 크기.
const imageWidth = 918;
const imageHeight = 541;

const LeafletMap = () => {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);

  useEffect(() => {
    // 지도가 여러 번 초기화되는 것을 방지
    if (mapInstance.current) return;

    // 지도를 담을 컨테이너가 필요
    if (mapRef.current) {
      // L.CRS.Simple을 사용하여 평면 이미지에 대한 좌표계를 설정.
      // 이를 통해 간단한 [y, x] 좌표를 사용할 수 있음.
      // 이미지 경계를 정의. 좌표는 [y, x] 형식.
      const bounds = [[0, 0], [imageHeight, imageWidth]];

      mapInstance.current = L.map(mapRef.current, {
        crs: L.CRS.Simple,
        minZoom: -2, // 필요에 따라 줌 레벨 조정
        zoomControl: false, // 확대/축소 버튼 비활성화
        maxBounds: bounds, // 맵 이동을 이미지 경계로 제한
        maxBoundsViscosity: 1.0, // 경계 밖으로 드래그 방지
      });

      const map = mapInstance.current;
      
      // 이미지 오버레이를 생성하여 지도에 추가
      L.imageOverlay(mapImageUrl, bounds).addTo(map);

      // 초기 뷰를 이미지 중앙으로 설정하고 줌 레벨을 0으로 지정
      map.setView([imageHeight / 2, imageWidth / 2], 0);
    }

    // 컴포넌트가 언마운트될 때 맵 인스턴스를 파괴하는 정리 함수
    return () => {
      if (mapInstance.current) {
        mapInstance.current.remove();
        mapInstance.current = null;
      }
    };
  }, []);

  return <div ref={mapRef} style={{ width: '100%', height: '100%' }} />;
};

export default LeafletMap;
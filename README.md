FastAPI 환경 구성:
	•	FastAPI, google-generativeai, dotenv 등을 설치하고 프로젝트 환경 세팅.
	•	.env 파일에 Google Generative AI API 키 저장.
튜닝된 모델과 통신:
	•	google.generativeai 라이브러리의 generate_message 메서드 활용.
	•	튜닝된 모델 ID와 API 키를 사용하여 프롬프트 기반으로 응답 생성.
	•	FastAPI를 통해 사용자 질문을 처리하고 모델에서 응답 반환.
프롬프트 설계:
	•	기본 프롬프트로 다음 내용을 설정:

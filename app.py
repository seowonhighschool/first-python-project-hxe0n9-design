import streamlit as st

# --- 1. 기본 설정 (세로형 키오스크 구현을 위해 좁은 레이아웃 사용) ---
st.set_page_config(page_title="K-Guide 시니어 키오스크", layout="centered")

# --- 2. 실제 키오스크 화면 구조를 복제하기 위한 디자인 설정 ---
st.markdown("""
    <style>
    /* 웹 페이지 전체 배경을 어둡게 처리 */
    .stApp { background-color: #0f172a; }
    
    /* 실제 무인 단말기 모니터 모양의 세로 틀 정의 */
    .kiosk-container {
        background-color: #ffffff;
        border: 12px solid #334155;
        border-radius: 20px;
        box-shadow: 0px 25px 50px rgba(0,0,0,0.6);
        max-width: 460px;
        margin: 0 auto;
        min-height: 800px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    /* 실제 키오스크 상단 파란색 타이틀 바 */
    .kiosk-header-blue {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        text-align: center;
        padding: 20px;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }
    
    /* 어르신 가이드용 빨간색 자막 바 */
    .kiosk-red-hint {
        background-color: #dc2626;
        color: white;
        text-align: center;
        padding: 12px;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    
    /* 가운데 메뉴 및 선택지들이 배치되는 구역 */
    .kiosk-main-content {
        padding: 20px;
        background-color: #ffffff;
    }
    
    /* 실제 키오스크 하단의 검은색 장바구니/결제 영역 */
    .kiosk-bottom-footer {
        background-color: #1e293b;
        color: white;
        padding: 20px;
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        border-top: 4px solid #e2e8f0;
    }
    
    /* 텍스트 크기 가독성 강화 */
    .item-title { font-size: 22px !important; font-weight: bold !important; color: #1e293b; text-align: center; margin-bottom: 2px; }
    .item-price-text { font-size: 18px !important; font-weight: bold !important; color: #2563eb; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 3. 데이터 저장 변수 초기화 ---
if "page" not in st.session_state:
    st.session_state.page = "shop_select" # 첫 화면: 매장 선택
    st.session_state.step = "menu_select"  # 단계: menu_select -> option_select -> checkout -> complete
    st.session_state.shop_type = ""       # fastfood(버거) 또는 cafe(커피)
    st.session_state.selected_item = ""   # 선택한 메뉴 이름
    st.session_state.final_price = 0      # 최종 결제 금액
    st.session_state.sub_option = ""       # 세트 여부 또는 HOT/ICE

# ==========================================
# 📱 실제 세로형 키오스크 인터페이스 빌드
# ==========================================

# [A] 상단 영역 정의 (가게 선택 페이지 여부에 따라 다르게 출력)
if st.session_state.page == "shop_select":
    st.markdown('<div class="kiosk-header-blue">🏠 K-Guide 무인 결제기</div>', unsafe_allow_html=True)
    st.markdown('<div class="kiosk-red-hint">💡 연습하고 싶으신 매장을 터치해 주세요.</div>', unsafe_allow_html=True)
else:
    shop_title = "🍔 패스트푸드 매장" if st.session_state.shop_type == "fastfood" else "☕ 커피 전문 매장"
    st.markdown(f'<div class="kiosk-header-blue">{shop_title}</div>', unsafe_allow_html=True)
    
    # 진행 단계별 빨간색 힌트 자막 변경
    if st.session_state.step == "menu_select":
        hint_text = "💡 원하시는 메뉴 버튼을 손가락으로 눌러주세요."
    elif st.session_state.step == "option_select":
        hint_text = "💡 원하시는 추가 옵션을 하나 골라주세요."
    elif st.session_state.step == "checkout":
        hint_text = "💡 맨 아래 장바구니의 초록색 [결제하기]를 누르세요."
    else:
        hint_text = "🎉 결제가 완료되었습니다!"
    st.markdown(f'<div class="kiosk-red-hint">{hint_text}</div>', unsafe_allow_html=True)


# [B] 가운데 콘텐츠 영역 (버튼 및 선택지들이 위치하는 곳)
st.markdown('<div class="kiosk-main-content">', unsafe_allow_html=True)

# 가게 내부 화면일 때만 네비게이션(뒤로가기/처음으로) 상단바 배치
if st.session_state.page == "main_kiosk":
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ 뒤로 이동", use_container_width=True):
            if st.session_state.step == "menu_select":
                st.session_state.page = "shop_select"
            elif st.session_state.step == "option_select":
                st.session_state.step = "menu_select"
            elif st.session_state.step == "checkout":
                st.session_state.step = "option_select"
            st.rerun()
    with col_nav2:
        if st.button("🏠 처음 화면", use_container_width=True):
            st.session_state.page = "shop_select"
            st.rerun()
    st.write("---")

# --- 1단계: 메인 장소 선택 화면 ---
if st.session_state.page == "shop_select":
    st.write("\n\n")
    if st.button("🍔\n\n패스트푸드점 (버거 연습 시작)", use_container_width=True, type="primary"):
        st.session_state.page = "main_kiosk"
        st.session_state.shop_type = "fastfood"
        st.session_state.step = "menu_select"
        st.rerun()
        
    st.write("\n\n")
    if st.button("☕\n\n커피 전문점 (카페 연습 시작)", use_container_width=True, type="secondary"):
        st.session_state.page = "main_kiosk"
        st.session_state.shop_type = "cafe"
        st.session_state.step = "menu_select"
        st.rerun()

# --- 2단계: 각 매장별 상품 고르기 화면 ---
elif st.session_state.page == "main_kiosk":
    
    # (2-1) 메뉴판 선택 단계
    if st.session_state.step == "menu_select":
        col1, col2 = st.columns(2)
        
        if st.session_state.shop_type == "fastfood":
            with col1:
                st.markdown('<p class="item-title">불고기버거</p><p class="item-price-text">4,500원</p>', unsafe_allow_html=True)
                if st.button("불고기버거 선택", use_container_width=True, type="primary"):
                    st.session_state.selected_item = "불고기버거"
                    st.session_state.final_price = 4500
                    st.session_state.step = "option_select"
                    st.rerun()
            with col2:
                st.markdown('<p class="item-title">치즈버거</p><p class="item-price-text">5,000원</p>', unsafe_allow_html=True)
                if st.button("치즈버거 선택", use_container_width=True, type="primary"):
                    st.session_state.selected_item = "치즈버거"
                    st.session_state.final_price = 5000
                    st.session_state.step = "option_select"
                    st.rerun()
            st.write("---")
            col3, _ = st.columns(2)
            with col3:
                st.markdown('<p class="item-title">새우버거</p><p class="item-price-text">4,800원</p>', unsafe_allow_html=True)
                if st.button("새우버거 선택", use_container_width=True, type="primary"):
                    st.session_state.selected_item = "새우버거"
                    st.session_state.final_price = 4800
                    st.session_state.step = "option_select"
                    st.rerun()
                    
        elif st.session_state.shop_type == "cafe":
            with col1:
                st.markdown('<p class="item-title">아메리카노</p><p class="item-price-text">3,000원</p>', unsafe_allow_html=True)
                if st.button("아메리카노 선택", use_container_width=True, type="primary"):
                    st.session_state.selected_item = "아메리카노"
                    st.session_state.final_price = 3000
                    st.session_state.step = "option_select"
                    st.rerun()
            with col2:
                st.markdown('<p class="item-title">카페라떼</p><p class="item-price-text">3,800원</p>', unsafe_allow_html=True)
                if st.button("카페라떼 선택", use_container_width=True, type="primary"):
                    st.session_state.selected_item = "카페라떼"
                    st.session_state.final_price = 3800
                    st.session_state.step = "option_select"
                    st.rerun()

    # (2-2) 세트 구성 또는 HOT / ICE 세부 옵션 선택 단계
    elif st.session_state.step == "option_select":
        st.write(f"### 🛒 선택하신 메뉴: **{st.session_state.selected_item}**")
        st.write("\n---")
        
        if st.session_state.shop_type == "fastfood":
            st.write("🍟 사이드와 음료를 추가하여 세트로 주문하시겠습니까?")
            if st.button("🥤 세트 변경 (+2,000원 추가)", use_container_width=True, type="primary"):
                st.session_state.sub_option = "세트"
                st.session_state.final_price += 2000
                st.session_state.step = "checkout"
                st.rerun()
            if st.button("🍔 버거 단품으로 그냥 먹기", use_container_width=True):
                st.session_state.sub_option = "단품"
                st.session_state.step = "checkout"
                st.rerun()
                
        elif st.session_state.shop_type == "cafe":
            st.write("❄️☀️ 마실 음료의 온도를 선택해 주세요.")
            if st.button("🔥 따뜻하게 주문 (HOT)", use_container_width=True, type="primary"):
                st.session_state.sub_option = "HOT"
                st.session_state.step = "checkout"
                st.rerun()
            if st.button("❄️ 차갑게 주문 (ICE)", use_container_width=True, type="secondary"):
                st.session_state.sub_option = "ICE"
                st.session_state.step = "checkout"
                st.rerun()

    # (2-3) 최종 장바구니 대기 상태 안내문
    elif st.session_state.step == "checkout":
        st.write("### 💳 메뉴 확인이 완료되었습니다.")
        st.write("화면 맨 아래 짙은 회색 공간에 생겨난 **[초록색 카드 결제하기]** 버튼을 꾹 눌러주세요!")
        st.write("\n\n")
        if st.button("❌ 처음부터 다시 고르기", use_container_width=True):
            st.session_state.step = "menu_select"
            st.session_state.selected_item = ""
            st.session_state.final_price = 0
            st.rerun()

    # (2-4) 결제 완료 성공 단계
    elif st.session_state.step == "complete":
        st.balloons()
        st.markdown('<h2 style="text-align:center; color:#16a34a;">🎉 주문 결제 성공 🎉</h2>', unsafe_allow_html=True)
        st.write("### 실제 매장 키오스크처럼 신용카드와 영수증을 단말기 구역에서 반드시 회수해 가세요!")
        st.write("\n\n")
        if st.button("🔄 처음으로 돌아가기 (새 연습)", use_container_width=True, type="primary"):
            st.session_state.page = "shop_select"
            st.session_state.step = "menu_select"
            st.session_state.selected_item = ""
            st.session_state.final_price = 0
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True) # 콘텐츠 구역 종료


# [C] 하단 고정 영역 (실제 키오스크 기기 하단 장바구니 및 투입구 모방)
if st.session_state.page == "main_kiosk":
    st.markdown('<div class="kiosk-bottom-footer">', unsafe_allow_html=True)
    st.write("### 🛒 주문 장바구니 명세서")
    
    if st.session_state.selected_item != "":
        st.write(f"▶ 선택된 상품: **{st.session_state.selected_item} ({st.session_state.sub_option})**")
        st.write(f"### 💵 총 합계 금액: {st.session_state.final_price:,}원")
        
        # 마지막 최종 checkout 단계일 때만 기기 하단 바에 녹색 결제 버튼 강제 노출
        if st.session_state.step == "checkout":
            st.write("\n")
            if st.button(f"🟩 💳 {st.session_state.final_price:,}원 카드 결제하기 (클릭) 🟩", use_container_width=True):
                st.session_state.step = "complete"
                st.rerun()
    else:
        st.write("현재 선택된 상품이 없습니다.")
    st.markdown('</div>', unsafe_allow_html=True)
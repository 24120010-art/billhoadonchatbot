import streamlit as st
from datetime import datetime
from openai import OpenAI


# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Quán Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="wide"
)


# ============================================================
# HIỂN THỊ ẢNH
# ============================================================

try:
    st.image(
        "4b48768552747ad1d57982cce438db69.jpg",
        use_container_width=True
    )
except:
    pass


# ============================================================
# DỮ LIỆU MENU
# ============================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu đường đen": 35000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 32000,
    "Trà sữa ô long": 33000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000
}


# ============================================================
# DỮ LIỆU TOPPING
# ============================================================

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 8000,
    "Trân châu hoàng kim": 7000
}


# ============================================================
# GIÁ SIZE
# ============================================================

SIZE_PRICE = {
    "M": 0,
    "L": 5000
}


# ============================================================
# DỮ LIỆU CALO THAM KHẢO
# ============================================================

CALORIES = {
    "Trà sữa truyền thống": 300,
    "Trà sữa trân châu đường đen": 420,
    "Trà sữa matcha": 280,
    "Trà sữa socola": 380,
    "Trà sữa khoai môn": 360,
    "Trà sữa dâu": 300,
    "Trà sữa ô long": 260,
    "Trà đào": 180,
    "Trà vải": 190,
    "Trà chanh": 120
}


# ============================================================
# TOPPING PHÙ HỢP
# ============================================================

SUITABLE_TOPPINGS = {

    "Trà sữa truyền thống": [
        "Trân châu đen",
        "Trân châu trắng",
        "Pudding trứng"
    ],

    "Trà sữa trân châu đường đen": [
        "Trân châu đen",
        "Trân châu hoàng kim",
        "Kem cheese"
    ],

    "Trà sữa matcha": [
        "Trân châu trắng",
        "Pudding trứng",
        "Kem cheese"
    ],

    "Trà sữa socola": [
        "Trân châu đen",
        "Pudding trứng",
        "Kem cheese"
    ],

    "Trà sữa khoai môn": [
        "Trân châu trắng",
        "Pudding trứng",
        "Kem cheese"
    ],

    "Trà sữa dâu": [
        "Trân châu trắng",
        "Thạch trái cây",
        "Pudding trứng"
    ],

    "Trà sữa ô long": [
        "Trân châu đen",
        "Trân châu trắng",
        "Thạch dừa"
    ],

    "Trà đào": [
        "Thạch trái cây",
        "Thạch dừa",
        "Trân châu trắng"
    ],

    "Trà vải": [
        "Thạch trái cây",
        "Thạch dừa",
        "Trân châu trắng"
    ],

    "Trà chanh": [
        "Thạch trái cây",
        "Thạch dừa"
    ]
}


# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = []


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("📋 Hệ thống tính hóa đơn")

st.divider()


# ============================================================
# THÔNG TIN KHÁCH HÀNG
# ============================================================

st.header("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Nhập tên khách hàng..."
)

st.session_state.customer_name = customer_name

st.divider()


# ============================================================
# CHỌN MÓN
# ============================================================

st.header("🧋 Chọn món")

col1, col2 = st.columns(2)


# ============================================================
# CỘT 1
# ============================================================

with col1:

    drink = st.selectbox(
        "Loại trà sữa / thức uống",
        list(MENU.keys())
    )

    size = st.radio(
        "Size ly",
        ["M", "L"],
        horizontal=True
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )


# ============================================================
# CỘT 2
# ============================================================

with col2:

    sugar = st.selectbox(
        "Mức độ đường",
        [
            "100% đường",
            "70% đường",
            "50% đường",
            "30% đường",
            "0% đường"
        ]
    )

    ice = st.selectbox(
        "Mức độ đá",
        [
            "100% đá",
            "70% đá",
            "50% đá",
            "30% đá",
            "Không đá"
        ]
    )

    toppings = st.multiselect(
        "Thêm topping",
        list(TOPPINGS.keys())
    )


# ============================================================
# TÍNH GIÁ
# ============================================================

drink_price = MENU[drink]

size_price = SIZE_PRICE[size]

topping_price = sum(
    TOPPINGS[topping]
    for topping in toppings
)

unit_price = (
    drink_price
    + size_price
    + topping_price
)

total_item = unit_price * quantity


# ============================================================
# HIỂN THỊ GIÁ
# ============================================================

st.info(
    f"💰 Đơn giá: **{unit_price:,} VNĐ/ly**  |  "
    f"Thành tiền: **{total_item:,} VNĐ**"
)


# ============================================================
# THÊM MÓN
# ============================================================

if st.button(
    "➕ Thêm món vào hóa đơn",
    use_container_width=True
):

    if not customer_name.strip():

        st.warning(
            "⚠️ Vui lòng nhập tên khách hàng trước."
        )

    else:

        item = {
            "drink": drink,
            "size": size,
            "sugar": sugar,
            "ice": ice,
            "toppings": toppings.copy(),
            "quantity": quantity,
            "unit_price": unit_price,
            "total": total_item
        }

        st.session_state.cart.append(item)

        st.success(
            f"✅ Đã thêm {quantity} ly "
            f"{drink} size {size} vào hóa đơn!"
        )


st.divider()


# ============================================================
# GIỎ HÀNG
# ============================================================

st.header("🛒 Danh sách món đã chọn")


if len(st.session_state.cart) == 0:

    st.info(
        "Chưa có món nào trong hóa đơn."
    )

else:

    grand_total = 0

    for i, item in enumerate(
        st.session_state.cart
    ):

        grand_total += item["total"]

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [5, 2, 1]
            )


            # ------------------------------------------------
            # THÔNG TIN MÓN
            # ------------------------------------------------

            with col1:

                st.markdown(
                    f"### 🧋 {i + 1}. "
                    f"{item['drink']}"
                )

                topping_text = (
                    ", ".join(item["toppings"])
                    if item["toppings"]
                    else "Không có topping"
                )

                st.write(
                    f"**Size:** {item['size']} | "
                    f"**Đường:** {item['sugar']} | "
                    f"**Đá:** {item['ice']}"
                )

                st.write(
                    f"**Topping:** {topping_text}"
                )


            # ------------------------------------------------
            # GIÁ
            # ------------------------------------------------

            with col2:

                st.write(
                    f"**Số lượng:** "
                    f"{item['quantity']} ly"
                )

                st.write(
                    f"**Đơn giá:** "
                    f"{item['unit_price']:,} VNĐ"
                )

                st.write(
                    f"**Thành tiền:** "
                    f"{item['total']:,} VNĐ"
                )


            # ------------------------------------------------
            # XÓA
            # ------------------------------------------------

            with col3:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{i}"
                ):

                    st.session_state.cart.pop(i)

                    st.rerun()


    st.divider()


    # ========================================================
    # TỔNG THANH TOÁN
    # ========================================================

    st.markdown(
        f"""
        <div style="
            background-color:#fff3cd;
            padding:20px;
            border-radius:10px;
            text-align:right;
        ">

            <h2>TỔNG THANH TOÁN</h2>

            <h1 style="color:#d63384;">
                {grand_total:,} VNĐ
            </h1>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")


    # ========================================================
    # THANH TOÁN
    # ========================================================

    if st.button(
        "💳 THANH TOÁN",
        type="primary",
        use_container_width=True
    ):

        if not customer_name.strip():

            st.warning(
                "⚠️ Vui lòng nhập tên khách hàng."
            )

        else:

            st.session_state.paid = True

            st.rerun()


# ============================================================
# HÓA ĐƠN
# ============================================================

if st.session_state.paid:

    st.divider()

    st.success(
        "🎉 Thanh toán thành công!"
    )

    st.header(
        "🧾 HÓA ĐƠN THANH TOÁN"
    )


    invoice_time = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


    # --------------------------------------------------------
    # ĐẦU HÓA ĐƠN
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div style="
            border:2px solid #333;
            padding:25px;
            border-radius:12px;
            background-color:white;
        ">

            <div style="text-align:center;">

                <h1>🧋 QUÁN TRÀ SỮA</h1>

                <p>HÓA ĐƠN THANH TOÁN</p>

            </div>

            <hr>

            <p>
                <b>Khách hàng:</b>
                {customer_name}
            </p>

            <p>
                <b>Thời gian:</b>
                {invoice_time}
            </p>

            <hr>
        """,
        unsafe_allow_html=True
    )


    invoice_total = 0


    # --------------------------------------------------------
    # CHI TIẾT HÓA ĐƠN
    # --------------------------------------------------------

    for i, item in enumerate(
        st.session_state.cart
    ):

        invoice_total += item["total"]

        topping_text = (
            ", ".join(item["toppings"])
            if item["toppings"]
            else "Không có"
        )


        st.markdown(
            f"""
            <div style="
                padding:10px;
                border-bottom:1px solid #ddd;
            ">

                <b>
                    {i + 1}. {item['drink']}
                </b>
                <br>

                Size: {item['size']} |
                Số lượng: {item['quantity']} ly
                <br>

                Đường: {item['sugar']} |
                Đá: {item['ice']}
                <br>

                Topping: {topping_text}
                <br>

                Đơn giá:
                {item['unit_price']:,} VNĐ
                <br>

                <b>
                    Thành tiền:
                    {item['total']:,} VNĐ
                </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # TỔNG HÓA ĐƠN
    # --------------------------------------------------------

    st.markdown(
        f"""
            <hr>

            <div style="text-align:right;">

                <h2>TỔNG CỘNG</h2>

                <h1 style="color:#d63384;">
                    {invoice_total:,} VNĐ
                </h1>

            </div>

            <hr>

            <div style="text-align:center;">

                <h3>
                    💗 Cảm ơn quý khách
                    đã sử dụng dịch vụ!
                </h3>

                <p>
                    Hẹn gặp lại quý khách 🧋
                </p>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    # ========================================================
    # TẠO ĐƠN MỚI
    # ========================================================

    if st.button(
        "🔄 TẠO ĐƠN MỚI",
        use_container_width=True
    ):

        st.session_state.cart = []

        st.session_state.paid = False

        st.session_state.customer_name = ""

        st.session_state.ai_chat_history = []

        st.rerun()


# ============================================================
# ============================================================
# 🤖 CHATBOT AI
# ============================================================
# ============================================================

st.divider()

st.header("🤖 Chatbot AI tư vấn trà sữa")

st.write(
    "💬 Hãy hỏi AI về menu, giá, topping, "
    "mức đường, calo hoặc nhờ AI tư vấn món phù hợp."
)


# ============================================================
# KIỂM TRA API KEY
# ============================================================

if "OPENAI_API_KEY" not in st.secrets:

    st.warning(
        "⚠️ Chatbot AI chưa được cấu hình API Key."
    )

    st.info(
        "Hãy tạo file "
        "`.streamlit/secrets.toml` "
        "và thêm OPENAI_API_KEY."
    )

else:

    # --------------------------------------------------------
    # KẾT NỐI OPENAI
    # --------------------------------------------------------

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )


    # ========================================================
    # CHUYỂN MENU THÀNH VĂN BẢN
    # ========================================================

    menu_text = "\n".join(
        [
            f"- {name}: {price:,} VNĐ/ly size M"
            for name, price in MENU.items()
        ]
    )


    # ========================================================
    # CHUYỂN TOPPING THÀNH VĂN BẢN
    # ========================================================

    topping_text = "\n".join(
        [
            f"- {name}: {price:,} VNĐ"
            for name, price in TOPPINGS.items()
        ]
    )


    # ========================================================
    # CHUYỂN SIZE THÀNH VĂN BẢN
    # ========================================================

    size_text = "\n".join(
        [
            f"- Size {size}: +{price:,} VNĐ"
            for size, price in SIZE_PRICE.items()
        ]
    )


    # ========================================================
    # DỮ LIỆU CALO
    # ========================================================

    calorie_text = "\n".join(
        [
            f"- {name}: khoảng {cal} kcal/ly size M"
            for name, cal in CALORIES.items()
        ]
    )


    # ========================================================
    # TOPPING PHÙ HỢP
    # ========================================================

    suitable_topping_text = "\n".join(
        [
            f"- {drink}: {', '.join(toppings)}"
            for drink, toppings
            in SUITABLE_TOPPINGS.items()
        ]
    )


    # ========================================================
    # PROMPT CHO AI
    # ========================================================

    AI_INSTRUCTIONS = f"""
Bạn là chatbot AI tư vấn khách hàng cho QUÁN TRÀ SỮA.

Nhiệm vụ của bạn:

1. Tư vấn đồ uống.
2. Tư vấn giá.
3. Tư vấn size.
4. Tư vấn topping.
5. Tư vấn mức đường.
6. Tư vấn mức đá.
7. So sánh các món.
8. Tư vấn theo ngân sách.
9. Tư vấn theo sở thích của khách.
10. Trả lời các câu hỏi về menu.
11. Có thể gợi ý món phù hợp dựa trên nhu cầu khách hàng.

Phong cách trả lời:

- Nói tiếng Việt.
- Thân thiện.
- Tự nhiên.
- Dễ hiểu.
- Không trả lời quá dài.
- Có thể sử dụng emoji.
- Không được bịa ra món ăn hoặc giá.
- Nếu thông tin không có trong dữ liệu thì phải nói rõ.
- Không tự tạo thêm sản phẩm ngoài menu.

========================
MENU
========================

{menu_text}


========================
TOPPING
========================

{topping_text}


========================
SIZE
========================

{size_text}


========================
MỨC ĐƯỜNG
========================

- 100% đường
- 70% đường
- 50% đường
- 30% đường
- 0% đường


========================
MỨC ĐÁ
========================

- 100% đá
- 70% đá
- 50% đá
- 30% đá
- Không đá


========================
CALO THAM KHẢO
========================

{calorie_text}

Lưu ý:
Thông tin calo chỉ là số liệu tham khảo
được dùng trong ứng dụng demo.
Không được khẳng định đây là số liệu
dinh dưỡng chính thức.


========================
TOPPING PHÙ HỢP
========================

{suitable_topping_text}


========================
CÁC DẠNG CÂU HỎI
========================

Khách có thể hỏi:

- Loại trà sữa nào giá cao nhất?
- Món nào giá thấp nhất?
- Món nào nhiều calo?
- Món nào ít calo?
- Trà sữa matcha giá bao nhiêu?
- Trà sữa matcha hợp topping gì?
- Em thích ít ngọt thì uống gì?
- Em có 40.000 VNĐ thì uống gì?
- Em muốn một món khoảng 35.000 VNĐ.
- Size L giá bao nhiêu?
- Thêm trân châu đen bao nhiêu tiền?
- Topping nào rẻ nhất?
- Topping nào đắt nhất?
- Em thích vị ngọt thì nên uống gì?
- Em thích vị thanh thì chọn món nào?
- Tư vấn một món cho em.


========================
NGUYÊN TẮC TÍNH GIÁ
========================

Giá size M = giá trong MENU.

Giá size L =
giá size M + 5.000 VNĐ.

Giá cuối cùng =
giá thức uống
+ giá size
+ giá tất cả topping.

Nếu khách hỏi tổng tiền,
hãy tính toán dựa trên các dữ liệu trên.


========================
QUAN TRỌNG
========================

Bạn là nhân viên tư vấn của quán.

Hãy trả lời như một nhân viên thật,
không nói rằng bạn là hệ thống rule-based.

Nếu khách hỏi câu ngoài phạm vi menu,
hãy trả lời lịch sự rằng bạn chỉ có thể
tư vấn các sản phẩm hiện có của quán.
"""


    # ========================================================
    # HIỂN THỊ LỊCH SỬ CHAT
    # ========================================================

    for message in st.session_state.ai_chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # ========================================================
    # CÂU HỎI GỢI Ý
    # ========================================================

    st.markdown("### 💡 Câu hỏi gợi ý")


    col_a, col_b, col_c = st.columns(3)


    suggested_question = None


    with col_a:

        if st.button(
            "💰 Giá cao nhất?",
            use_container_width=True
        ):

            suggested_question = (
                "Loại trà sữa nào có giá cao nhất?"
            )


    with col_b:

        if st.button(
            "🍮 Tư vấn topping",
            use_container_width=True
        ):

            suggested_question = (
                "Trà sữa matcha nên thêm topping nào?"
            )


    with col_c:

        if st.button(
            "🥤 Món ít ngọt",
            use_container_width=True
        ):

            suggested_question = (
                "Em thích uống ít ngọt, hãy "
                "tư vấn cho em một vài món phù hợp."
            )


    # ========================================================
    # Ô NHẬP CHAT
    # ========================================================

    user_question = st.chat_input(
        "💬 Nhập câu hỏi cho AI..."
    )


    # ========================================================
    # NẾU CHỌN CÂU HỎI GỢI Ý
    # ========================================================

    if suggested_question is not None:

        user_question = suggested_question


    # ========================================================
    # GỬI CÂU HỎI CHO AI
    # ========================================================

    if user_question:

        # ----------------------------------------------------
        # LƯU CÂU HỎI
        # ----------------------------------------------------

        st.session_state.ai_chat_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )


        # ----------------------------------------------------
        # HIỂN THỊ CÂU HỎI
        # ----------------------------------------------------

        with st.chat_message("user"):

            st.markdown(
                user_question
            )


        # ----------------------------------------------------
        # CHUẨN BỊ LỊCH SỬ HỘI THOẠI
        # ----------------------------------------------------

        conversation = []

        for message in st.session_state.ai_chat_history:

            conversation.append(
                {
                    "role": message["role"],
                    "content": message["content"]
                }
            )


        # ----------------------------------------------------
        # GỌI OPENAI RESPONSES API
        # ----------------------------------------------------

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    "🤖 AI đang suy nghĩ..."
                ):

                    response = client.responses.create(

                        model="gpt-5.6-luna",

                        instructions=AI_INSTRUCTIONS,

                        input=conversation,

                        max_output_tokens=500
                    )


                    answer = response.output_text


                    st.markdown(
                        answer
                    )


            # ------------------------------------------------
            # LƯU CÂU TRẢ LỜI
            # ------------------------------------------------

            st.session_state.ai_chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception as e:

            st.error(
                "❌ Không thể kết nối với AI."
            )

            st.caption(
                f"Chi tiết lỗi: {str(e)}"
            )


    # ========================================================
    # XÓA LỊCH SỬ CHAT
    # ========================================================

    if len(
        st.session_state.ai_chat_history
    ) > 0:

        if st.button(
            "🗑️ Xóa lịch sử trò chuyện",
            use_container_width=True
        ):

            st.session_state.ai_chat_history = []

            st.rerun()

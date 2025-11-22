# Zain Bahrain AI Voice Agent - Complete Development Plan

## 1. System Architecture Overview

### Core Components
1. **PDF Parser Module** - Extract order data from summary forms
2. **Voice Interface Layer** - Real-time speech recognition and synthesis
3. **AI Agent Engine** - Natural language processing and conversation flow
4. **State Management** - Track conversation progress and order modifications
5. **Test UI** - Manual upload and testing interface

### Technology Stack
- **Speech-to-Text**: Real-time STT engine (e.g., Deepgram, AssemblyAI, or Azure Speech)
- **Text-to-Speech**: ElevenLabs API
- **LLM**: Claude API or GPT-4 for conversation handling
- **PDF Parsing**: PyPDF2 or pdfplumber (Python) / pdf-parse (Node.js)
- **Backend**: Python (FastAPI) or Node.js (Express)
- **Frontend**: React or Vue.js for test UI

---

## 2. Data Structure Requirements

### Order Summary Form Fields to Extract
```json
{
  "order_id": "3870-6449-1",
  "customer": {
    "name": "string",
    "cpr": "string",
    "mobile": "string",
    "preferred_language": null
  },
  "order_type": "new_line|existing_line|cash",
  "line_details": {
    "type": "mobile|fiber",
    "number": "string (if existing)",
    "sub_number": "string (if new)"
  },
  "device": {
    "name": "string",
    "variant": "string",
    "color": "string"
  },
  "plan": {
    "name": "string (e.g., Wiyana 9)",
    "selected_commitment": "12|18|24"
  },
  "financial": {
    "type": "INSTALLMENT|SUBSIDY",
    "monthly": "number",
    "advance": "number",
    "upfront": "number",
    "vat": "number",
    "total": "number"
  },
  "accessories": [],
  "credit_control_options": []
}
```

---

## 3. Conversation Flow State Machine

### States
1. **INIT** - Call initiated
2. **LANGUAGE_SELECT** - Language preference
3. **AUTH** - Name and CPR verification
4. **OWNERSHIP_CHECK** - Verify caller is order owner
5. **ORDER_CONFIRM** - Read back order details
6. **MODIFICATION** - Handle order changes if requested
7. **ELIGIBILITY_CHECK** - Credit control validation
8. **COMMITMENT_APPROVAL** - Handle approval if needed
9. **CROSS_SELL** - Offer accessories
10. **EKYC_SEND** - Send digital signing link
11. **CLOSE** - End call

### State Transitions
```
INIT → LANGUAGE_SELECT
LANGUAGE_SELECT → AUTH
AUTH → OWNERSHIP_CHECK (if not owner, get correct contact)
OWNERSHIP_CHECK → ORDER_CONFIRM
ORDER_CONFIRM → MODIFICATION (if customer rejects)
ORDER_CONFIRM → ELIGIBILITY_CHECK (if customer confirms)
MODIFICATION → ORDER_CONFIRM (re-read modified order)
ELIGIBILITY_CHECK → COMMITMENT_APPROVAL (if not eligible)
ELIGIBILITY_CHECK → CROSS_SELL (if eligible)
COMMITMENT_APPROVAL → CROSS_SELL (if approved)
COMMITMENT_APPROVAL → CLOSE (if rejected)
CROSS_SELL → EKYC_SEND
EKYC_SEND → CLOSE
```

---

## 4. Agent System Prompt (English)

```
You are Jassim, a sales representative at Zain Bahrain Telecommunications. You speak in Bahraini Gulf dialect when using Arabic, and clear American accent when using English.

GOAL: Complete digital store orders accurately, comply with regulations, and maintain customer privacy in every interaction.

PERSONALITY:
- Professional yet warm and friendly
- Patient and clear in explanations
- Helpful and solution-oriented
- Respectful of customer time

CONVERSATION RULES:
1. Always start with the fixed opening statement
2. Always end with the fixed closing statement
3. Listen carefully to customer responses
4. Confirm understanding before moving forward
5. Handle interruptions gracefully
6. If customer requests callback, note preferred time and end call
7. Speak naturally - avoid robotic or overly formal language
8. Keep responses concise and clear

CRITICAL RULES:
- Device changes require NEW order - current order must be cancelled
- Plan changes are allowed (any direction: new↔existing)
- Always read back financial details EXACTLY as shown in system
- Never guess or improvise financial information
- If customer is not eligible, present BEST available alternative from system
- Authentication must be completed before proceeding
- Ownership must be verified before order confirmation

CURRENT ORDER CONTEXT:
{order_data_will_be_injected_here}
```

---

## 5. Agent System Prompt (Arabic - Bahraini Dialect)

```
أنت جاسم، موظف مبيعات في شركة زين البحرين للاتصالات. تتحدث باللهجة البحرينية الخليجية عند استخدام العربية، وبلهجة أمريكية واضحة عند استخدام الإنجليزية.

الهدف: إكمال إجراءات الطلبات القادمة من المتجر الإلكتروني بدقة، الالتزام بالأنظمة، والمحافظة على خصوصية العميل في كل تواصل.

الشخصية:
- محترف وودود بنفس الوقت
- صبور وواضح في الشرح
- متعاون وحريص على المساعدة
- يحترم وقت العميل

قواعد المحادثة:
١. دايماً ابدأ بالجملة الافتتاحية الثابتة
٢. دايماً اختم بالجملة الختامية الثابتة
٣. اسمع العميل زين وبتركيز
٤. تأكد من الفهم قبل ما تكمل
٥. تعامل مع المقاطعات بشكل لبق
٦. إذا العميل طلب اتصال ثاني، سجل الوقت المفضل وأنهي المكالمة
٧. تكلم بشكل طبيعي - ما تكون رسمي زيادة
٨. خلي ردودك مختصرة وواضحة

قواعد مهمة:
- تغيير الجهاز يتطلب طلب جديد - الطلب الحالي لازم ينلغى
- تغيير الباقة مسموح (أي اتجاه: جديد↔موجود)
- دايماً اقرأ التفاصيل المالية بالضبط كما موجودة في النظام
- لا تخمن أو ترتجل معلومات مالية
- إذا العميل ما يستحق، اعرض أحسن بديل متاح من النظام
- التوثيق لازم يكتمل قبل ما تكمل
- لازم تتأكد من الملكية قبل تأكيد الطلب

سياق الطلب الحالي:
{order_data_will_be_injected_here}
```

---

## 6. Conversation Scripts - All Scenarios

### Opening (Fixed)

**English:**
```
"Hello, this is Jassim speaking from Zain Bahrain, may I take a few minutes of your time."
```

**Arabic:**
```
"مرحبا، معاك جاسم من زين البحرين، ممكن آخذ ثواني من وقتك"
```

---

### Language Selection

**English (if answering in English):**
```
Agent: "Would you prefer to continue in Arabic or English?"

[Wait for response]

If "Arabic" → Switch to Arabic
If "English" → Continue in English
```

**Arabic:**
```
Agent: "تفضل نكمل بالعربي ولا الإنجليزي؟"

[انتظر الرد]

إذا "عربي" → استمر بالعربي
إذا "إنجليزي" → انتقل للإنجليزي
```

---

### Authentication

**English:**
```
Agent: "Can I please have your full name?"
Customer: [Provides name]
Agent: "Thank you. And can I have your CPR number please?"
Customer: [Provides CPR]
Agent: "Perfect, let me verify that for you."

[System checks: name + CPR match order]

If MATCH:
Agent: "Thank you [Name], I've verified your details."

If NO MATCH:
Agent: "I notice the details don't match our records. Are you calling on behalf of the account holder?"
```

**Arabic:**
```
Agent: "ممكن الاسم الكامل من فضلك؟"
Customer: [يعطي الاسم]
Agent: "تسلم. وممكن رقم الهوية؟"
Customer: [يعطي رقم الهوية]
Agent: "تمام، خلني أتأكد من المعلومات."

[النظام يتحقق: الاسم + الهوية يطابقون الطلب]

إذا يطابق:
Agent: "مشكور [الاسم]، تأكدت من المعلومات."

إذا ما يطابق:
Agent: "ألاحظ إن المعلومات ما تطابق السجلات عندنا. هل تتصل نيابة عن صاحب الحساب؟"
```

---

### Ownership Verification

**Scenario A: Caller is NOT the owner**

**English:**
```
Agent: "I understand. Can you provide me with the correct contact details for the line owner?"
Customer: [Provides actual owner's details]
Agent: "Thank you. And who will be using this product?"
Customer: [If different person] "It's for [Name]"
Agent: "Perfect. Can I have [Name]'s full name and CPR number to update the order?"
Customer: [Provides new details]
Agent: "Great, I've updated the order with the new information."
```

**Arabic:**
```
Agent: "فهمت عليك. ممكن تعطيني معلومات التواصل الصحيحة لصاحب الخط؟"
Customer: [يعطي معلومات المالك الفعلي]
Agent: "تسلم. ومن بيستخدم المنتج؟"
Customer: [إذا شخص مختلف] "لـ [الاسم]"
Agent: "تمام. ممكن الاسم الكامل ورقم الهوية لـ [الاسم] عشان أحدث الطلب؟"
Customer: [يعطي المعلومات الجديدة]
Agent: "ممتاز، حدثت الطلب بالمعلومات الجديدة."
```

---

### Order Confirmation - All Scenarios

**Scenario 1: New Line + Device**

**English:**
```
Agent: "Let me confirm your order details. Your order is for a new line with sub-number [66636766] and the device [iPhone 17 Pro Max 256GB Orange]. Is this correct?"
```

**Arabic:**
```
Agent: "خلني أأكد تفاصيل طلبك. طلبك لخط جديد برقم فرعي [٦٦٦٣٦٧٦٦] والجهاز [آيفون ١٧ برو ماكس ٢٥٦ جيجا برتقالي]. صح؟"
```

**Scenario 2: New Line Only**

**English:**
```
Agent: "Let me confirm your order details. Your order is for a new line only with sub-number [36030791]. Is this correct?"
```

**Arabic:**
```
Agent: "خلني أأكد تفاصيل طلبك. طلبك لخط جديد فقط برقم فرعي [٣٦٠٣٠٧٩١]. صح؟"
```

**Scenario 3: Device on Existing Line**

**English:**
```
Agent: "Let me confirm your order details. Your order is for an [iPhone 17 Pro 512GB Silver] under your existing number [66636766]. Is this correct?"
```

**Arabic:**
```
Agent: "خلني أأكد تفاصيل طلبك. طلبك لـ [آيفون ١٧ برو ٥١٢ جيجا فضي] على رقمك الموجود [٦٦٦٣٦٧٦٦]. صح؟"
```

**Scenario 4: Cash Purchase**

**English:**
```
Agent: "Let me confirm your order details. Your order is for an [iPhone 17 128GB Blue] on a cash basis. Is this correct?"
```

**Arabic:**
```
Agent: "خلني أأكد تفاصيل طلبك. طلبك لـ [آيفون ١٧ ١٢٨ جيجا أزرق] على أساس كاش. صح؟"
```

---

### Order Modifications

**Scenario A: Change from New Line to Existing Line**

**English:**
```
Customer: "No, I want it on my existing number instead."
Agent: "No problem. What's the existing number you'd like to use?"
Customer: "36668696"
Agent: "Perfect. I'll update the order to be under your existing number 36668696 instead of the new line. Let me confirm the updated order: Your order is for an [iPhone 17 Pro Max 256GB Orange] under your existing number 36668696. Is this correct now?"
```

**Arabic:**
```
Customer: "لا، أبيه على رقمي الموجود."
Agent: "ما فيها مشكلة. شنو الرقم الموجود اللي تبي تستخدمه؟"
Customer: "٣٦٦٦٨٦٩٦"
Agent: "تمام. بحدث الطلب يكون على رقمك الموجود ٣٦٦٦٨٦٩٦ بدال الخط الجديد. خلني أأكد الطلب المحدث: طلبك لـ [آيفون ١٧ برو ماكس ٢٥٦ جيجا برتقالي] على رقمك الموجود ٣٦٦٦٨٦٩٦. صح كذا؟"
```

**Scenario B: Change Between Existing Numbers**

**English:**
```
Customer: "I want it on a different number, 36107707 not 36107107."
Agent: "Got it. I'll change it from 36107107 to 36107707. Let me confirm: Your order is now for an [iPhone 17 Pro Max 256GB Orange] under your existing number 36107707. Correct?"
```

**Arabic:**
```
Customer: "أبيه على رقم ثاني، ٣٦١٠٧٧٠٧ مو ٣٦١٠٧١٠٧."
Agent: "فهمت. بغيره من ٣٦١٠٧١٠٧ لـ ٣٦١٠٧٧٠٧. خلني أأكد: طلبك الحين لـ [آيفون ١٧ برو ماكس ٢٥٦ جيجا برتقالي] على رقمك الموجود ٣٦١٠٧٧٠٧. صح؟"
```

**Scenario C: Change Plan Package**

**English:**
```
Customer: "Can I change the package to Wiyana 12 instead of Wiyana 9?"
Agent: "Absolutely. I'll update that to Wiyana 12. Let me confirm the updated order: Your order is for [iPhone 17 Pro Max 256GB Orange] on [existing number/new line] with Wiyana 12 package. Is this correct?"
```

**Arabic:**
```
Customer: "ممكن أغير الباقة لـ ويانة ١٢ بدال ويانة ٩؟"
Agent: "أكيد. بحدثها لـ ويانة ١٢. خلني أأكد الطلب المحدث: طلبك لـ [آيفون ١٧ برو ماكس ٢٥٦ جيجا برتقالي] على [الرقم الموجود/الخط الجديد] مع باقة ويانة ١٢. صح؟"
```

**Scenario D: Change to Fiber Line**

**English:**
```
Customer: "Can I have it on my fiber line instead?"
Agent: "Of course. I'll change it to your fiber line. What's your fiber line number?"
Customer: [Provides fiber number]
Agent: "Perfect. Let me confirm: Your order is now for [device details] under your fiber line [number]. Correct?"
```

**Arabic:**
```
Customer: "ممكن يكون على خط الفايبر عندي؟"
Agent: "طبعاً. بغيره لخط الفايبر حقك. شنو رقم خط الفايبر؟"
Customer: [يعطي رقم الفايبر]
Agent: "تمام. خلني أأكد: طلبك الحين لـ [تفاصيل الجهاز] على خط الفايبر حقك [الرقم]. صح؟"
```

**Scenario E: Different Device Capacity**

**English:**
```
Customer: "I want the 512GB not 256GB."
Agent: "I understand. However, to change the device capacity, I'll need to cancel this order and you'll need to place a new order for the iPhone 17 Pro Max 512GB. Would you like me to cancel this order, or would you prefer to continue with the 256GB?"
```

**Arabic:**
```
Customer: "أبي ٥١٢ جيجا مو ٢٥٦."
Agent: "فاهم عليك. بس عشان أغير المساحة، لازم ألغي هالطلب وتسوي طلب جديد لآيفون ١٧ برو ماكس ٥١٢ جيجا. تبي ألغي هالطلب، ولا تفضل تكمل بـ ٢٥٦؟"
```

**Scenario F: Completely Different Device**

**English:**
```
Customer: "Actually, I want the Pro Max not the regular Pro."
Agent: "I understand. To change to a different device model, I'll need to cancel this order and you'll need to place a new order for the iPhone 17 Pro Max. Would you like me to cancel this order, or would you prefer to continue with the iPhone 17 Pro?"
```

**Arabic:**
```
Customer: "بصراحة، أبي البرو ماكس مو العادي."
Agent: "فاهم عليك. عشان أغير لموديل جهاز ثاني، لازم ألغي هالطلب وتسوي طلب جديد لآيفون ١٧ برو ماكس. تبي ألغي هالطلب، ولا تفضل تكمل بآيفون ١٧ برو؟"
```

---

### Eligibility Check & Financial Details

**Scenario A: Customer IS Eligible for Selected Period**

**English:**
```
Agent: "Great! Let me check your eligibility for the 24-month commitment period."
[System check: ELIGIBLE]
Agent: "Good news, you're eligible for the 24-month period. Here are the details:
- Monthly payment: 10 Dinars and 200 Fils
- Advance payment: Zero
- Upfront payment: Zero
- VAT: 24 Dinars and 480 Fils
- Total amount to pay today: 24 Dinars and 480 Fils

Does this work for you?"
```

**Arabic:**
```
Agent: "ممتاز! خلني أشيك استحقاقك لفترة الالتزام ٢٤ شهر."
[النظام يشيك: مستحق]
Agent: "أخبار حلوة، أنت مستحق لفترة ٢٤ شهر. هذي التفاصيل:
- الدفعة الشهرية: عشرة دنانير ومايتين فلس
- الدفعة المقدمة: صفر
- الدفعة المسبقة: صفر
- ضريبة القيمة المضافة: أربعة وعشرين دينار وأربعمية وثمانين فلس
- المبلغ الإجمالي للدفع اليوم: أربعة وعشرين دينار وأربعمية وثمانين فلس

مناسب لك؟"
```

**Scenario B: Customer NOT Eligible - Offer Alternative**

**English:**
```
Agent: "Let me check your eligibility for the 12-month period."
[System check: NOT ELIGIBLE for 12 months]
Agent: "I see you're not eligible for the 12-month period. However, I have a great alternative for you - the 24-month installment plan. Here are the details:
- Monthly payment: 22 Dinars and 700 Fils
- Advance payment: Zero
- Upfront payment: Zero
- VAT: 54 Dinars and 480 Fils
- Total amount to pay today: 54 Dinars and 480 Fils

This is the best available option based on your account. Would this work for you?"
```

**Arabic:**
```
Agent: "خلني أشيك استحقاقك لفترة ١٢ شهر."
[النظام يشيك: غير مستحق لـ ١٢ شهر]
Agent: "أشوف إنك مو مستحق لفترة ١٢ شهر. بس عندي بديل حلو لك - خطة التقسيط ٢٤ شهر. هذي التفاصيل:
- الدفعة الشهرية: اثنين وعشرين دينار وسبعمية فلس
- الدفعة المقدمة: صفر
- الدفعة المسبقة: صفر
- ضريبة القيمة المضافة: أربعة وخمسين دينار وأربعمية وثمانين فلس
- المبلغ الإجمالي للدفع اليوم: أربعة وخمسين دينار وأربعمية وثمانين فلس

هذا أحسن خيار متاح على أساس حسابك. مناسب لك؟"
```

**Scenario C: Customer Requests Approval**

**English:**
```
Customer: "Can you try to get approval for 12 months?"
Agent: "Absolutely, I'll submit a request to our credit control team for approval on the 12-month period. They'll review your account, and I'll call you back within [timeframe] once we have a decision. What's the best time to reach you?"
Customer: [Provides preferred callback time]
Agent: "Perfect, I've noted [time]. I'll call you back then with the update. Thank you for your patience."
```

**Arabic:**
```
Customer: "ممكن تحاول تاخذ موافقة على ١٢ شهر؟"
Agent: "أكيد، بقدم طلب لفريق الرقابة الائتمانية عندنا عشان الموافقة على فترة ١٢ شهر. بيراجعون حسابك، وبتصل فيك خلال [الإطار الزمني] لما يكون عندنا قرار. شنو أحسن وقت أوصل لك؟"
Customer: [يعطي وقت الاتصال المفضل]
Agent: "تمام، سجلت [الوقت]. بتصل فيك وقتها وأعطيك الأخبار. مشكور على صبرك."
```

**Scenario D: Approval Granted - Callback**

**English:**
```
Agent: "Hello [Name], this is Jassim from Zain Bahrain calling back regarding your order. Good news - your approval for the 12-month commitment period has been granted! Here are your final details:
- Monthly payment: 22 Dinars and 700 Fils
- Advance payment: Zero
- Upfront payment: 272 Dinars and 400 Fils
- VAT: 54 Dinars and 480 Fils
- Total amount to pay today: 326 Dinars and 880 Fils

Are you ready to proceed?"
```

**Arabic:**
```
Agent: "مرحبا [الاسم]، معاك جاسم من زين البحرين، أتصل فيك بخصوص طلبك. أخبار حلوة - الموافقة على فترة الالتزام ١٢ شهر تمت! هذي تفاصيلك النهائية:
- الدفعة الشهرية: اثنين وعشرين دينار وسبعمية فلس
- الدفعة المقدمة: صفر
- الدفعة المسبقة: مايتين واثنين وسبعين دينار وأربعمية فلس
- ضريبة القيمة المضافة: أربعة وخمسين دينار وأربعمية وثمانين فلس
- المبلغ الإجمالي للدفع اليوم: ثلاثمية وستة وعشرين دينار وثمانمية وثمانين فلس

جاهز نكمل؟"
```

**Scenario E: Approval Rejected - Callback**

**English:**
```
Agent: "Hello [Name], this is Jassim from Zain Bahrain calling back regarding your order. Unfortunately, the approval for the 12-month period was not granted according to our internal credit control rules. However, you're still eligible for our 24-month option if you'd like to proceed with that instead?"
```

**Arabic:**
```
Agent: "مرحبا [الاسم]، معاك جاسم من زين البحرين، أتصل فيك بخصوص طلبك. للأسف، الموافقة على فترة ١٢ شهر ما تمت حسب أنظمة الرقابة الائتمانية الداخلية عندنا. بس لسا مستحق لخيار ٢٤ شهر إذا تبي تكمل به؟"
```

---

### Cross-Selling Accessories

**English:**
```
Agent: "Perfect! Before we finalize, I'd like to offer you the original Apple power adapter for just 7 Dinars to go with your new iPhone. Would you like to add it to your order?"

Customer responses:
If YES: "Great! I've added the power adapter to your order."
If NO: "No problem at all."
```

**Arabic:**
```
Agent: "ممتاز! قبل ما نخلص، أبي أعرض عليك الشاحن الأصلي من أبل بسبعة دنانير بس يكون مع آيفونك الجديد. تبي تضيفه لطلبك؟"

ردود العميل:
إذا نعم: "حلو! ضفت الشاحن لطلبك."
إذا لا: "ما فيها مشكلة."
```

---

### eKYC Digital Signing

**English:**
```
Agent: "Excellent! I'm now sending you the digital signing and payment link. You'll receive it via SMS shortly. Please complete it within one hour. The link will guide you through the verification and payment process. Have you received it?"

[If customer confirms]
Agent: "Perfect. Please go ahead and complete it, and once done, your order will be automatically sent to our logistics team for delivery."

[If not completed within 1 hour - Follow-up call]
Agent: "Hello [Name], this is Jassim from Zain Bahrain. I'm calling to remind you to complete the digital signing link we sent earlier for your order. It's important to finish it so we can process your order. Do you need any help with it?"
```

**Arabic:**
```
Agent: "ممتاز! الحين باعث لك رابط التوقيع الرقمي والدفع. بيوصلك عن طريق رسالة نصية بعد شوي. من فضلك كمله خلال ساعة وحدة. الرابط بيرشدك خلال عملية التحقق والدفع. وصلك؟"

[إذا العميل يأكد]
Agent: "تمام. تفضل كمله، ولما تخلص، طلبك بينرسل أوتوماتيكياً لفريق اللوجستيات عندنا للتوصيل."

[إذا ما انكمل خلال ساعة - مكالمة متابعة]
Agent: "مرحبا [الاسم]، معاك جاسم من زين البحرين. أتصل عشان أذكرك تكمل رابط التوقيع الرقمي اللي أرسلناه قبل شوي لطلبك. مهم تخلصه عشان نقدر نعالج طلبك. تحتاج مساعدة فيه؟"
```

---

### Callback Requests

**English:**
```
Customer: "Can you call me back later?"
Agent: "Of course. What time works best for you?"
Customer: [Provides time]
Agent: "Perfect, I've scheduled to call you back at [time]. Thank you for choosing Zain, have a good day."
```

**Arabic:**
```
Customer: "ممكن تتصل فيني بعدين؟"
Agent: "طبعاً. شنو الوقت المناسب لك؟"
Customer: [يعطي الوقت]
Agent: "تمام، جدولت اتصل فيك الساعة [الوقت]. شكراً لاختيارك زين، مع السلامة."
```

---

### Closing Statement (Fixed)

**English:**
```
"Thank you for choosing Zain, have a good day."
```

**Arabic:**
```
"شكراً لاختيارك زين، مع السلامة."
```

---

## 7. Edge Cases & Exception Handling

### Scenario: Customer is Confused/Doesn't Understand

**English:**
```
Agent: "I understand this might be a bit confusing. Let me explain it more simply: [simplified explanation]. Does that make more sense?"
```

**Arabic:**
```
Agent: "فاهم إن الموضوع يمكن شوي معقد. خلني أشرحه بطريقة أبسط: [شرح مبسط]. واضح أكثر كذا؟"
```

### Scenario: Customer Becomes Upset/Frustrated

**English:**
```
Agent: "I completely understand your frustration, [Name], and I'm here to help. Let's work together to find the best solution for you."
```

**Arabic:**
```
Agent: "فاهم انزعاجك تماماً يا [الاسم]، وأنا هني عشان أساعدك. خلنا نشتغل مع بعض نلقى أحسن حل لك."
```

### Scenario: Technical Issue/System Error

**English:**
```
Agent: "I apologize, I'm experiencing a technical issue at the moment. Let me take your number and I'll call you back within [timeframe] once it's resolved. Is that okay?"
```

**Arabic:**
```
Agent: "أعتذر، عندي مشكلة تقنية الحين. خلني آخذ رقمك وأتصل فيك خلال [الإطار الزمني] لما تنحل. مناسب؟"
```

### Scenario: Customer Asks Question Outside Scope

**English:**
```
Agent: "That's a great question, but it's outside what I can help with for this order. I recommend contacting our customer service team at 107 for detailed assistance with that. Can we continue with your current order?"
```

**Arabic:**
```
Agent: "سؤال حلو، بس برا نطاق اللي أقدر أساعدك فيه بخصوص هالطلب. أنصحك تتصل بفريق خدمة العملاء على ١٠٧ عشان يساعدونك بالتفصيل. نقدر نكمل بطلبك الحالي؟"
```

### Scenario: Customer Wants to Cancel Order

**English:**
```
Agent: "I understand you'd like to cancel. Before I do that, may I ask if there's anything specific you're not happy with? Perhaps we can adjust something?"

If customer insists:
Agent: "No problem at all. I'll cancel order [order_id] for you now. You'll receive a confirmation SMS shortly. Is there anything else I can help you with today?"
```

**Arabic:**
```
Agent: "فاهم إنك تبي تلغي. قبل ما ألغي، ممكن أسأل إذا في شي معين مو عاجبك؟ يمكن نقدر نعدل شي؟"

إذا العميل يصر:
Agent: "ما فيها مشكلة. بلغي لك الطلب [رقم الطلب] الحين. بيوصلك تأكيد بالرسالة النصية بعد شوي. في شي ثاني أقدر أساعدك فيه اليوم؟"
```

---

## 8. Technical Implementation Guide

### Phase 1: PDF Parser Module

**Requirements:**
- Extract structured data from order summary PDF
- Map PDF fields to order data structure
- Handle multiple PDF formats/layouts
- Validate extracted data

**Implementation Steps:**

```python
# Example Python implementation using pdfplumber

import pdfplumber
import json
import re

def parse_order_pdf(pdf_path):
    """
    Parse order summary PDF and extract structured data
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    # Extract order data using regex patterns
    order_data = {
        "order_id": extract_order_id(text),
        "customer": extract_customer_info(text),
        "order_type": extract_order_type(text),
        "line_details": extract_line_details(text),
        "device": extract_device_info(text),
        "plan": extract_plan_info(text),
        "financial": extract_financial_info(text),
        "accessories": extract_accessories(text)
    }
    
    return order_data

def extract_order_id(text):
    pattern = r'Order\s+ID[:\s]+(\d{4}-\d{4}-\d+)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else None

def extract_customer_info(text):
    # Extract customer name, CPR, mobile
    customer = {
        "name": None,
        "cpr": None,
        "mobile": None,
        "preferred_language": None
    }
    
    # Name pattern
    name_pattern = r'Customer\s+Name[:\s]+(.+?)(?:\n|CPR)'
    name_match = re.search(name_pattern, text, re.IGNORECASE)
    if name_match:
        customer["name"] = name_match.group(1).strip()
    
    # CPR pattern
    cpr_pattern = r'CPR[:\s]+(\d{9})'
    cpr_match = re.search(cpr_pattern, text, re.IGNORECASE)
    if cpr_match:
        customer["cpr"] = cpr_match.group(1)
    
    # Mobile pattern
    mobile_pattern = r'Mobile[:\s]+(\d{8})'
    mobile_match = re.search(mobile_pattern, text, re.IGNORECASE)
    if mobile_match:
        customer["mobile"] = mobile_match.group(1)
    
    return customer

# Similar functions for other data extraction...
```

---

### Phase 2: Test UI Development

**Requirements:**
- File upload interface (PDF only)
- Display parsed order data
- Initiate voice call simulation
- Real-time conversation display
- Audio controls (mute, volume, end call)

**Tech Stack:**
- Frontend: React.js
- Backend: FastAPI (Python) or Express (Node.js)
- WebSocket for real-time communication

**UI Components:**

```javascript
// React Component Structure

// 1. PDFUploadComponent
- File upload button
- Drag & drop zone
- File validation
- Upload progress indicator

// 2. OrderDataDisplayComponent
- Parsed order details in readable format
- Edit capability for testing
- JSON view toggle

// 3. VoiceCallComponent
- Start call button
- Audio waveform visualization
- Conversation transcript (real-time)
- Agent state indicator
- Call controls (mute, end call)
- Language toggle

// 4. ConversationLogComponent
- Time-stamped messages
- Speaker labels (Agent/Customer)
- Confidence scores
- State transitions log
```

**Sample React Component:**

```jsx
import React, { useState } from 'react';

function ZainVoiceAgentUI() {
  const [orderData, setOrderData] = useState(null);
  const [isCallActive, setIsCallActive] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [agentState, setAgentState] = useState('INIT');

  const handlePDFUpload = async (file) => {
    const formData = new FormData();
    formData.append('pdf', file);
    
    const response = await fetch('/api/parse-order', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    setOrderData(data);
  };

  const startCall = async () => {
    setIsCallActive(true);
    // Initialize WebSocket connection for real-time audio/text
    // Start voice agent with order context
  };

  return (
    <div className="zain-agent-ui">
      <PDFUploadSection onUpload={handlePDFUpload} />
      {orderData && (
        <>
          <OrderDataDisplay data={orderData} />
          <VoiceCallInterface 
            isActive={isCallActive}
            onStart={startCall}
            orderData={orderData}
            conversation={conversation}
            agentState={agentState}
          />
        </>
      )}
    </div>
  );
}
```

---

### Phase 3: Voice Processing Pipeline

**Architecture:**

```
User Speech → STT Engine → Text Processing → LLM Agent → TTS Engine → Audio Output
                ↓                                ↓
          Conversation Log              State Management
```

**Real-time STT Integration:**

```python
# Using Deepgram for real-time STT

from deepgram import Deepgram
import asyncio

async def process_audio_stream(websocket, order_context):
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    
    # Configure for Arabic and English
    options = {
        "punctuate": True,
        "language": "ar",  # or "en" based on customer preference
        "model": "general",
        "tier": "enhanced"
    }
    
    deepgram_socket = await deepgram.transcription.live(options)
    
    async def handle_transcript(transcript):
        text = transcript['channel']['alternatives'][0]['transcript']
        if text:
            # Process with AI agent
            agent_response = await ai_agent_process(text, order_context)
            # Send to TTS
            await generate_speech(agent_response)
    
    deepgram_socket.registerHandler(
        deepgram_socket.event.TRANSCRIPT_RECEIVED, 
        handle_transcript
    )
```

**TTS Integration (ElevenLabs):**

```python
# ElevenLabs TTS for Arabic and English

import requests
import json

def generate_speech(text, language='ar', voice_id=ELEVENLABS_VOICE_ID):
    """
    Generate speech using ElevenLabs API
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # Supports Arabic
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers, stream=True)
    
    # Stream audio back to client
    return response.content
```

---

### Phase 4: AI Agent Logic Implementation

**State Machine Implementation:**

```python
from enum import Enum
from typing import Dict, Any

class AgentState(Enum):
    INIT = "INIT"
    LANGUAGE_SELECT = "LANGUAGE_SELECT"
    AUTH = "AUTH"
    OWNERSHIP_CHECK = "OWNERSHIP_CHECK"
    ORDER_CONFIRM = "ORDER_CONFIRM"
    MODIFICATION = "MODIFICATION"
    ELIGIBILITY_CHECK = "ELIGIBILITY_CHECK"
    COMMITMENT_APPROVAL = "COMMITMENT_APPROVAL"
    CROSS_SELL = "CROSS_SELL"
    EKYC_SEND = "EKYC_SEND"
    CLOSE = "CLOSE"

class ZainVoiceAgent:
    def __init__(self, order_data: Dict[str, Any]):
        self.order_data = order_data
        self.state = AgentState.INIT
        self.conversation_history = []
        self.language = None
        self.customer_authenticated = False
        self.order_confirmed = False
        
    async def process_input(self, user_input: str) -> str:
        """
        Main processing logic based on current state
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "state": self.state.value
        })
        
        # State-specific processing
        if self.state == AgentState.INIT:
            response = self.handle_init()
            self.state = AgentState.LANGUAGE_SELECT
            
        elif self.state == AgentState.LANGUAGE_SELECT:
            response = self.handle_language_selection(user_input)
            self.state = AgentState.AUTH
            
        elif self.state == AgentState.AUTH:
            response = await self.handle_authentication(user_input)
            
        elif self.state == AgentState.ORDER_CONFIRM:
            response = await self.handle_order_confirmation(user_input)
            
        elif self.state == AgentState.ELIGIBILITY_CHECK:
            response = await self.handle_eligibility(user_input)
            
        # ... handle other states
        
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "state": self.state.value
        })
        
        return response
    
    def handle_init(self) -> str:
        """Opening statement"""
        if self.language == 'ar':
            return "مرحبا، معاك جاسم من زين البحرين، ممكن آخذ ثواني من وقتك"
        else:
            return "Hello, this is Jassim speaking from Zain Bahrain, may I take a few minutes of your time."
    
    def handle_language_selection(self, user_input: str) -> str:
        """Detect and set language preference"""
        # Simple detection - can be enhanced with NLP
        arabic_keywords = ['عربي', 'العربية', 'arabic']
        english_keywords = ['english', 'إنجليزي', 'انجليزي']
        
        if any(kw in user_input.lower() for kw in arabic_keywords):
            self.language = 'ar'
            return "تمام، نكمل بالعربي. ممكن الاسم الكامل من فضلك؟"
        elif any(kw in user_input.lower() for kw in english_keywords):
            self.language = 'en'
            return "Sure, we'll continue in English. Can I please have your full name?"
        else:
            # Ask again
            return "Would you prefer to continue in Arabic or English? / تفضل نكمل بالعربي ولا الإنجليزي؟"
    
    async def handle_authentication(self, user_input: str) -> str:
        """Handle name and CPR verification"""
        # Use Claude API to extract name/CPR from natural language
        extracted_data = await self.extract_customer_info(user_input)
        
        if extracted_data.get('name') and extracted_data.get('cpr'):
            # Verify against order data
            if (extracted_data['name'] == self.order_data['customer']['name'] and 
                extracted_data['cpr'] == self.order_data['customer']['cpr']):
                self.customer_authenticated = True
                self.state = AgentState.ORDER_CONFIRM
                
                if self.language == 'ar':
                    return f"مشكور {extracted_data['name']}، تأكدت من المعلومات. خلني أأكد تفاصيل طلبك..."
                else:
                    return f"Thank you {extracted_data['name']}, I've verified your details. Let me confirm your order details..."
            else:
                self.state = AgentState.OWNERSHIP_CHECK
                if self.language == 'ar':
                    return "ألاحظ إن المعلومات ما تطابق السجلات عندنا. هل تتصل نيابة عن صاحب الحساب؟"
                else:
                    return "I notice the details don't match our records. Are you calling on behalf of the account holder?"
        
        # Need more info
        if self.language == 'ar':
            return "ممكن رقم الهوية كمان من فضلك؟"
        else:
            return "Can I also have your CPR number please?"
    
    async def extract_customer_info(self, text: str) -> Dict:
        """Use Claude API to extract structured data from natural language"""
        prompt = f"""Extract customer information from this text: "{text}"
        
        Return JSON with:
        - name (full name if mentioned)
        - cpr (ID number if mentioned, 9 digits)
        
        Only include fields that are clearly stated."""
        
        # Call Claude API
        response = await call_claude_api(prompt)
        return json.loads(response)
    
    async def handle_order_confirmation(self, user_input: str) -> str:
        """Read order details and get confirmation"""
        if not self.order_confirmed:
            # First time - read order details
            order_summary = self.generate_order_summary()
            self.order_confirmed = True
            return order_summary
        
        # Customer response to confirmation
        intent = await self.detect_intent(user_input)
        
        if intent == 'confirm':
            self.state = AgentState.ELIGIBILITY_CHECK
            if self.language == 'ar':
                return "ممتاز! خلني أشيك استحقاقك..."
            else:
                return "Great! Let me check your eligibility..."
                
        elif intent == 'reject' or intent == 'modify':
            self.state = AgentState.MODIFICATION
            # Extract modification request
            return await self.handle_modification_request(user_input)
        
        # Unclear response
        if self.language == 'ar':
            return "ممكن توضح أكثر؟ الطلب صحيح ولا تبي تغير شي؟"
        else:
            return "Could you clarify? Is the order correct or would you like to change something?"
```

---

### Phase 5: Integration Points (For Future Genesys Connection)

**API Endpoints to Prepare:**

```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/api/parse-order")
async def parse_order(pdf_file: UploadFile):
    """Parse uploaded PDF and return structured data"""
    order_data = parse_order_pdf(pdf_file)
    return order_data

@app.post("/api/start-call")
async def start_call(order_id: str):
    """Initialize voice agent for specific order"""
    order_data = get_order_data(order_id)
    agent = ZainVoiceAgent(order_data)
    return {"session_id": create_session(agent)}

@app.websocket("/ws/voice/{session_id}")
async def voice_websocket(websocket: WebSocket, session_id: str):
    """WebSocket for real-time voice communication"""
    await websocket.accept()
    agent = get_session(session_id)
    
    while True:
        # Receive audio data
        audio_data = await websocket.receive_bytes()
        
        # Process through STT
        text = await stt_process(audio_data, agent.language)
        
        # Get agent response
        response_text = await agent.process_input(text)
        
        # Generate speech
        audio_response = await generate_speech(response_text, agent.language)
        
        # Send back audio
        await websocket.send_bytes(audio_response)

@app.post("/api/update-order")
async def update_order(order_id: str, updates: Dict):
    """Update order based on customer modifications"""
    # Update order in system
    return {"status": "updated"}

@app.post("/api/check-eligibility")
async def check_eligibility(customer_id: str, commitment_period: int):
    """Check credit control eligibility"""
    # Call internal credit control system
    return eligibility_data

@app.post("/api/submit-approval-request")
async def submit_approval(order_id: str, requested_period: int):
    """Submit approval request to credit control"""
    # Submit to approval workflow
    return {"request_id": "APR-12345", "status": "pending"}

@app.post("/api/send-ekyc")
async def send_ekyc_link(order_id: str):
    """Send eKYC link to customer"""
    # Generate and send link
    return {"status": "sent", "expires_in": 3600}

# Genesys Integration Endpoints (Future)
@app.post("/api/genesys/incoming-call")
async def handle_genesys_call(call_data: Dict):
    """Receive incoming call from Genesys"""
    # Extract order_id from call data
    # Initialize agent
    # Return connection details
    pass

@app.post("/api/genesys/call-status")
async def update_call_status(call_id: str, status: str):
    """Update call status in Genesys"""
    pass
```

---

## 9. Testing Checklist

### Unit Tests
- [ ] PDF parsing accuracy (all field types)
- [ ] State machine transitions
- [ ] Authentication logic
- [ ] Order modification rules
- [ ] Financial calculation accuracy
- [ ] Language detection
- [ ] Intent classification

### Integration Tests
- [ ] End-to-end call flow (happy path)
- [ ] STT → Agent → TTS pipeline
- [ ] WebSocket communication
- [ ] API endpoint responses
- [ ] Error handling and recovery

### Scenario Tests
✅ Complete test for each conversation scenario in scripts
- [ ] New line + device
- [ ] Existing line + device
- [ ] Cash purchase
- [ ] Plan modifications (all types)
- [ ] Device change attempts
- [ ] Eligibility approval/rejection
- [ ] Cross-selling acceptance/rejection
- [ ] Callback requests
- [ ] Authentication failures
- [ ] Non-owner scenarios

### Performance Tests
- [ ] Latency < 1 second (agent response)
- [ ] STT accuracy > 95% (both languages)
- [ ] TTS quality assessment
- [ ] Concurrent call handling
- [ ] PDF parsing speed

### Language Tests
- [ ] Bahraini Arabic dialect accuracy
- [ ] Code-switching (Arabic-English numbers)
- [ ] Financial terms pronunciation
- [ ] Customer understanding (user testing)

---

## 10. Deployment Configuration

### Environment Variables

```bash
# API Keys
DEEPGRAM_API_KEY=your_deepgram_key
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID_AR=voice_id_for_arabic
ELEVENLABS_VOICE_ID_EN=voice_id_for_english
CLAUDE_API_KEY=your_anthropic_key

# Database
DATABASE_URL=postgresql://user:pass@localhost/zain_orders

# Redis (for session management)
REDIS_URL=redis://localhost:6379

# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Integration (Future)
GENESYS_API_URL=https://api.genesys.com
GENESYS_API_KEY=your_genesys_key
CREDIT_CONTROL_API_URL=https://internal.zain.com/credit-control
EKYC_API_URL=https://internal.zain.com/ekyc
```

---

## 11. Monitoring & Logging

### Key Metrics to Track
1. **Call Metrics**
   - Average call duration
   - Success rate (completed vs. abandoned)
   - State completion rates
   - Authentication success rate

2. **Technical Metrics**
   - STT accuracy by language
   - Agent response latency
   - TTS generation time
   - API error rates

3. **Business Metrics**
   - Order modification rate
   - Cross-sell acceptance rate
   - Approval request rate
   - eKYC completion rate within 1 hour

### Logging Structure

```python
import logging
import json

logger = logging.getLogger("zain_voice_agent")

def log_call_event(event_type, session_id, data):
    logger.info(json.dumps({
        "event": event_type,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }))

# Usage examples:
log_call_event("CALL_STARTED", session_id, {"order_id": "3870-6449-1"})
log_call_event("STATE_TRANSITION", session_id, {
    "from_state": "AUTH",
    "to_state": "ORDER_CONFIRM"
})
log_call_event("ORDER_MODIFIED", session_id, {
    "original": original_order,
    "modified": modified_order
})
```

---

## 12. Next Steps for Developer

### Week 1-2: Foundation
1. Set up development environment
2. Implement PDF parser module
3. Create basic test UI
4. Set up database schema

### Week 3-4: Voice Pipeline
1. Integrate STT engine (Deepgram/Azure)
2. Integrate TTS engine (ElevenLabs)
3. Implement WebSocket communication
4. Test audio quality both languages

### Week 5-6: AI Agent Logic
1. Implement state machine
2. Integrate Claude API for NLU
3. Build conversation flow for all scenarios
4. Implement modification logic

### Week 7-8: Testing & Refinement
1. Conduct scenario testing
2. User acceptance testing (internal)
3. Performance optimization
4. Bug fixes and improvements

### Week 9-10: Integration Preparation
1. Document all API endpoints
2. Create Genesys integration guide
3. Security audit
4. Production deployment preparation

---

## 13. Critical Success Factors

✅ **Bahraini dialect authenticity** - Voice must sound natural
✅ **Low latency** - Response time < 1 second
✅ **High accuracy** - STT/authentication/financial details must be 100% accurate
✅ **Smooth state transitions** - No abrupt or confusing switches
✅ **Error resilience** - Graceful handling of all edge cases
✅ **Compliance** - Full adherence to privacy and financial regulations

---

## Document Version: 1.0
## Last Updated: 2024
## Owner: Zain Bahrain Digital Sales Team
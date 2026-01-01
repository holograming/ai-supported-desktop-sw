-- TossPlace POS Sample Data
-- This file is for reference. Data is inserted via DatabaseManager.

-- Categories
INSERT INTO categories (name, icon, sort_order) VALUES
('커피', 'coffee', 1),
('음료', 'cup', 2),
('디저트', 'cake', 3),
('베이커리', 'bread', 4);

-- Products
INSERT INTO products (category_id, name, price, sort_order) VALUES
-- 커피 (category_id = 1)
(1, '아메리카노', 4500, 1),
(1, '카페라떼', 5000, 2),
(1, '바닐라라떼', 5500, 3),
(1, '카푸치노', 5000, 4),
(1, '에스프레소', 3500, 5),
(1, '카라멜마끼아또', 5500, 6),
(1, '콜드브루', 5000, 7),

-- 음료 (category_id = 2)
(2, '자몽에이드', 5500, 1),
(2, '레몬에이드', 5000, 2),
(2, '아이스티', 4500, 3),
(2, '밀크티', 5500, 4),
(2, '초코라떼', 5000, 5),

-- 디저트 (category_id = 3)
(3, '치즈케이크', 6500, 1),
(3, '티라미수', 7000, 2),
(3, '마카롱 세트', 8000, 3),
(3, '브라우니', 5500, 4),

-- 베이커리 (category_id = 4)
(4, '크로와상', 4000, 1),
(4, '베이글', 3500, 2),
(4, '머핀', 4500, 3),
(4, '스콘', 4000, 4);

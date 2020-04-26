SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ip
-- ----------------------------
DROP TABLE IF EXISTS `ip`;
CREATE TABLE `ip`  (
  `ip_start` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `ip_end` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `ip_start_num` bigint(20) NULL DEFAULT NULL,
  `ip_end_num` bigint(20) NULL DEFAULT NULL,
  `continent` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `country` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `province` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `city` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `district` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `isp` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `area_code` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `country_english` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `country_code` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `longitude` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `latitude` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  INDEX `idx_ip_start_num`(`ip_start_num`) USING BTREE,
  INDEX `idx_ip_end_num`(`ip_end_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ip
-- ----------------------------
INSERT INTO `ip` VALUES ('0.0.0.0', '0.255.255.255', 0, 16777215, '', '保留', '', '', '', '', '', '', '', '', '');
INSERT INTO `ip` VALUES ('1.0.0.0', '1.0.0.0', 16777216, 16777216, '', 'Cloudflare', '', '', '', 'CloudflareDNS/APNIC', '', '', '', '', '');
INSERT INTO `ip` VALUES ('1.0.0.1', '1.0.0.1', 16777217, 16777217, '', 'CloudFlareDNS', '', '', '', 'APNIC', '', '', '', '', '');
INSERT INTO `ip` VALUES ('1.0.0.2', '1.0.0.255', 16777218, 16777471, '大洋洲', '澳大利亚', '', '', '', '', '', 'Australia', 'AU', '133.775136', '-25.274398');
INSERT INTO `ip` VALUES ('1.0.1.0', '1.0.3.255', 16777472, 16778239, '亚洲', '中国', '福建', '福州', '', '电信', '350100', 'China', 'CN', '119.306239', '26.075302');
INSERT INTO `ip` VALUES ('1.0.4.0', '1.0.7.255', 16778240, 16779263, '大洋洲', '澳大利亚', '', '墨尔本', '', '', '', 'Australia', 'AU', '133.775136', '-25.274398');
INSERT INTO `ip` VALUES ('1.0.8.0', '1.0.15.255', 16779264, 16781311, '亚洲', '中国', '广东', '广州', '', '电信', '440100', 'China', 'CN', '113.280637', '23.125178');
INSERT INTO `ip` VALUES ('1.0.16.0', '1.0.31.255', 16781312, 16785407, '亚洲', '日本', '', '', '', '', '', 'Japan', 'JP', '138.252924', '36.204824');
INSERT INTO `ip` VALUES ('1.0.32.0', '1.0.63.255', 16785408, 16793599, '亚洲', '中国', '广东', '广州', '', '电信', '440100', 'China', 'CN', '113.280637', '23.125178');
INSERT INTO `ip` VALUES ('1.0.64.0', '1.0.79.255', 16793600, 16797695, '亚洲', '日本', '广岛', '', '', '', '', 'Japan', 'JP', '138.252924', '36.204824');

-- ----------------------------
-- Table structure for phone
-- ----------------------------
DROP TABLE IF EXISTS `phone`;
CREATE TABLE `phone`  (
  `prefix` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `province` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `city` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `isp` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `post_code` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `city_code` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `area_code` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  INDEX `idx_phone`(`phone`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of phone
-- ----------------------------
INSERT INTO `phone` VALUES ('130', '1300000', '山东', '济南', '联通', '250000', '0531', '370100');
INSERT INTO `phone` VALUES ('130', '1300001', '江苏', '常州', '联通', '213000', '0519', '320400');
INSERT INTO `phone` VALUES ('130', '1300002', '安徽', '巢湖', '联通', '238000', '0551', '340181');
INSERT INTO `phone` VALUES ('130', '1300003', '四川', '宜宾', '联通', '644000', '0831', '511500');
INSERT INTO `phone` VALUES ('130', '1300004', '四川', '自贡', '联通', '643000', '0813', '510300');
INSERT INTO `phone` VALUES ('130', '1300005', '陕西', '西安', '联通', '710000', '029', '610100');
INSERT INTO `phone` VALUES ('130', '1300006', '江苏', '南京', '联通', '210000', '025', '320100');
INSERT INTO `phone` VALUES ('130', '1300007', '陕西', '西安', '联通', '710000', '029', '610100');
INSERT INTO `phone` VALUES ('130', '1300008', '湖北', '武汉', '联通', '430000', '027', '420100');
INSERT INTO `phone` VALUES ('130', '1300009', '陕西', '西安', '联通', '710000', '029', '610100');

SET FOREIGN_KEY_CHECKS = 1;

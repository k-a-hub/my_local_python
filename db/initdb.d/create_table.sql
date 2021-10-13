use tamaya

CREATE TABLE IF NOT EXISTS `dtb_order` (
  `id` bigint(20) unsigned NOT NULL,
  `customer_id` int(10) unsigned DEFAULT NULL,
  `country_id` smallint(5) unsigned DEFAULT NULL,
  `pref_id` smallint(5) unsigned DEFAULT NULL,
  `sex_id` smallint(5) unsigned DEFAULT NULL,
  `job_id` smallint(5) unsigned DEFAULT NULL,
  `payment_id` int(10) unsigned DEFAULT NULL,
  `device_type_id` smallint(5) unsigned DEFAULT NULL,
  `pre_order_id` varchar(255) DEFAULT NULL,
  `order_no` varchar(255) DEFAULT NULL,
  `message` varchar(4000) DEFAULT NULL,
  `name01` varchar(255) NOT NULL,
  `name02` varchar(255) NOT NULL,
  `kana01` varchar(255) DEFAULT NULL,
  `kana02` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone_number` varchar(14) DEFAULT NULL,
  `postal_code` varchar(8) DEFAULT NULL,
  `addr01` varchar(255) DEFAULT NULL,
  `addr02` varchar(255) DEFAULT NULL,
  `birth` datetime DEFAULT NULL COMMENT '(DC2Type:datetimetz)',
  `subtotal` decimal(12,2) unsigned NOT NULL DEFAULT 0.00,
  `discount` decimal(12,2) unsigned NOT NULL DEFAULT 0.00,
  `delivery_fee_total` decimal(12,2) unsigned NOT NULL DEFAULT 0.00,
  `charge` decimal(12,2) unsigned NOT NULL DEFAULT 0.00,
  `tax` decimal(12,2) unsigned NOT NULL DEFAULT 0.00,
  `total` decimal(12,2) unsigned NOT NULL DEFAULT 0.00,
  `payment_total` decimal(12,2) unsigned NOT NULL DEFAULT 0.00,
  `payment_method` varchar(255) DEFAULT NULL,
  `note` varchar(4000) DEFAULT NULL,
  `create_date` datetime NOT NULL COMMENT '(DC2Type:datetimetz)',
  `update_date` datetime NOT NULL COMMENT '(DC2Type:datetimetz)',
  `order_date` datetime DEFAULT NULL COMMENT '(DC2Type:datetimetz)',
  `payment_date` datetime DEFAULT NULL COMMENT '(DC2Type:datetimetz)',
  `currency_code` varchar(255) DEFAULT NULL,
  `complete_message` longtext DEFAULT NULL,
  `complete_mail_message` longtext DEFAULT NULL,
  `add_point` decimal(12,0) unsigned NOT NULL DEFAULT 0,
  `use_point` decimal(12,0) unsigned NOT NULL DEFAULT 0,
  `order_status_id` smallint(5) unsigned DEFAULT NULL,
  `discriminator_type` varchar(255) NOT NULL,
  `shop_id` int(10) unsigned DEFAULT NULL,
  `floor_id` int(10) unsigned DEFAULT NULL,
  `agent_cd` int(10) unsigned DEFAULT NULL,
  `member_id` int(10) unsigned DEFAULT NULL,
  `sales_account_no` varchar(255) DEFAULT NULL,
  `ne_cooperation` int(11) DEFAULT NULL,
  `position` varchar(255) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=20123118211403249 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `dtb_order_item` (
  `id` int(10) unsigned NOT NULL,
  `order_id` bigint(20) unsigned DEFAULT NULL,
  `product_id` int(10) unsigned DEFAULT NULL,
  `product_class_id` int(10) unsigned DEFAULT NULL,
  `shipping_id` int(10) unsigned DEFAULT NULL,
  `rounding_type_id` smallint(5) unsigned DEFAULT NULL,
  `tax_type_id` smallint(5) unsigned DEFAULT NULL,
  `tax_display_type_id` smallint(5) unsigned DEFAULT NULL,
  `order_item_type_id` smallint(5) unsigned DEFAULT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_code` varchar(255) DEFAULT NULL,
  `class_name1` varchar(255) DEFAULT NULL,
  `class_name2` varchar(255) DEFAULT NULL,
  `class_category_name1` varchar(255) DEFAULT NULL,
  `class_category_name2` varchar(255) DEFAULT NULL,
  `price` decimal(12,2) NOT NULL DEFAULT 0.00,
  `quantity` decimal(10,0) NOT NULL DEFAULT 0,
  `tax` decimal(10,0) NOT NULL DEFAULT 0,
  `tax_rate` decimal(10,0) unsigned NOT NULL DEFAULT 0,
  `tax_adjust` decimal(10,0) unsigned NOT NULL DEFAULT 0,
  `tax_rule_id` smallint(5) unsigned DEFAULT NULL,
  `currency_code` varchar(255) DEFAULT NULL,
  `processor_name` varchar(255) DEFAULT NULL,
  `point_rate` decimal(10,0) unsigned DEFAULT NULL,
  `discriminator_type` varchar(255) NOT NULL,
  `option_set_flg` tinyint(1) DEFAULT NULL,
  `option_serial` varchar(10000) DEFAULT NULL,
  `custom_product_name` varchar(255) DEFAULT NULL,
  `accept_no` int(10) unsigned DEFAULT NULL,
  `page_no` smallint(5) unsigned DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=423345 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `dtb_shipping` (
  `id` int(10) unsigned NOT NULL,
  `order_id` bigint(20) unsigned DEFAULT NULL,
  `country_id` smallint(5) unsigned DEFAULT NULL,
  `pref_id` smallint(5) unsigned DEFAULT NULL,
  `delivery_id` int(10) unsigned DEFAULT NULL,
  `creator_id` int(10) unsigned DEFAULT NULL,
  `name01` varchar(255) NOT NULL,
  `name02` varchar(255) NOT NULL,
  `kana01` varchar(255) DEFAULT NULL,
  `kana02` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(14) DEFAULT NULL,
  `postal_code` varchar(8) DEFAULT NULL,
  `addr01` varchar(255) DEFAULT NULL,
  `addr02` varchar(255) DEFAULT NULL,
  `delivery_name` varchar(255) DEFAULT NULL,
  `time_id` int(10) unsigned DEFAULT NULL,
  `delivery_time` varchar(255) DEFAULT NULL,
  `delivery_date` datetime DEFAULT NULL COMMENT '(DC2Type:datetimetz)',
  `shipping_date` datetime DEFAULT NULL COMMENT '(DC2Type:datetimetz)',
  `tracking_number` varchar(255) DEFAULT NULL,
  `note` varchar(4000) DEFAULT NULL,
  `sort_no` smallint(5) unsigned DEFAULT NULL,
  `create_date` datetime NOT NULL COMMENT '(DC2Type:datetimetz)',
  `update_date` datetime NOT NULL COMMENT '(DC2Type:datetimetz)',
  `mail_send_date` datetime DEFAULT NULL COMMENT '(DC2Type:datetimetz)',
  `discriminator_type` varchar(255) NOT NULL,
  `gp_check` smallint(5) unsigned DEFAULT NULL,
  `gp_tie` smallint(5) unsigned DEFAULT NULL,
  `gp_kind` smallint(5) unsigned DEFAULT NULL,
  `gp_butuji` smallint(5) unsigned DEFAULT NULL,
  `gp_calendar` smallint(5) unsigned DEFAULT NULL,
  `gp_package` smallint(5) unsigned DEFAULT NULL,
  `gp_namechoice` smallint(5) unsigned DEFAULT NULL,
  `gp_sonota` smallint(5) unsigned DEFAULT NULL,
  `gp_title` varchar(255) DEFAULT NULL,
  `gp_name` varchar(255) DEFAULT NULL,
  `gp_birthday` varchar(255) DEFAULT NULL,
  `gp_inputsonota` varchar(255) DEFAULT NULL,
  `position` varchar(255) DEFAULT NULL,
  `delivery_month` varchar(255) DEFAULT NULL,
  `delivery_period` varchar(255) DEFAULT NULL,
  `office_delivery` tinyint(1) DEFAULT 0,
  `title` varchar(10) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=231659 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `dtb_customer_address` (
  `id` int(10) unsigned NOT NULL,
  `customer_id` int(10) unsigned DEFAULT NULL,
  `country_id` smallint(5) unsigned DEFAULT NULL,
  `pref_id` smallint(5) unsigned DEFAULT NULL,
  `name01` varchar(255) NOT NULL,
  `name02` varchar(255) NOT NULL,
  `kana01` varchar(255) DEFAULT NULL,
  `kana02` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `postal_code` varchar(8) DEFAULT NULL,
  `addr01` varchar(255) DEFAULT NULL,
  `addr02` varchar(255) DEFAULT NULL,
  `phone_number` varchar(14) DEFAULT NULL,
  `create_date` datetime NOT NULL COMMENT '(DC2Type:datetimetz)',
  `update_date` datetime NOT NULL COMMENT '(DC2Type:datetimetz)',
  `discriminator_type` varchar(255) NOT NULL,
  `position` varchar(255) DEFAULT NULL,
  `title` varchar(10) DEFAULT NULL,
  `accept_no` int(10) unsigned DEFAULT NULL,
  `page_no` smallint(5) unsigned DEFAULT NULL,
  `delete_end_season` tinyint(1) DEFAULT 0
) ENGINE=InnoDB AUTO_INCREMENT=99285 DEFAULT CHARSET=utf8;
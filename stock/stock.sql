CREATE TABLE `allstock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `code` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=3814 DEFAULT CHARSET=utf8 ;

CREATE TABLE `all_partition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `code` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=3814 DEFAULT CHARSET=utf8 ;

CREATE TABLE `partition_stock_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hd_date` varchar(25) NOT NULL,
  `partition_code` varchar(50) NOT NULL,
  `stock_code` varchar(10) NOT NULL,
  `close_price` float(20,5) DEFAULT NULL,
  `hold_sum` float(20,5) DEFAULT NULL,
  `hold_money` float(20,5) DEFAULT NULL,
  `today_zd` float(20,5) DEFAULT NULL,
  `hold_sum_percent` float(20,5) DEFAULT NULL,
  `hold_change_one` float(20,5) DEFAULT NULL,
  `hold_change_five` float(20,5) DEFAULT NULL,
  `hold_change_ten` float(20,5) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_dx` (`hd_date`,`partition_code`,`stock_code`)
) ENGINE=MyISAM AUTO_INCREMENT=3814 DEFAULT CHARSET=utf8 ;

CREATE TABLE `agg_partition_stock_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hd_date` varchar(25) NOT NULL,
  `partition_code` varchar(50) NOT NULL,
  `stock_code` varchar(10) NOT NULL,
  `stock_name` varchar(50) NOT NULL,
  `avg_hold_sum_one` float(20,5) DEFAULT NULL,
  `avg_hold_sum_three` float(20,5) DEFAULT NULL,
  `avg_hold_sum_five` float(20,5) DEFAULT NULL,
  `avg_hold_sum_ten` float(20,5) DEFAULT NULL,
  `avg_hold_sum_thirty` float(20,5) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_dx` (`hd_date`,`partition_code`,`stock_code`)
) ENGINE=MyISAM AUTO_INCREMENT=3814 DEFAULT CHARSET=utf8 ;


CREATE TABLE `rzrq_stock_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hd_date` varchar(25) NOT NULL,
  `stock_code` varchar(10) NOT NULL,
  `stock_name` varchar(50) NOT NULL,
  `close_price` float(20,5) DEFAULT NULL,
  `zdf` float(20,5) DEFAULT NULL,
  `rz_remain_sum` float(20,5) DEFAULT NULL,
  `rz_remain_sum_percent` float(20,5) DEFAULT NULL,
  `rq_remain_sum` float(20,5) DEFAULT NULL,
  `rq_margin` float(20,5) DEFAULT NULL,
  `rzrq_remain_sum` float(20,5) DEFAULT NULL,
  `rzrq_remain_sum_margin` float(20,5) DEFAULT NULL,
  `rz_buy_one` float(20,5) DEFAULT NULL,
  `rz_repay_one` float(20,5) DEFAULT NULL,
  `rz_net_buy_one` float(20,5) DEFAULT NULL,
  `rq_sell_one` float(20,5) DEFAULT NULL,
  `rq_repay_one` float(20,5) DEFAULT NULL,
  `rq_net_sell_one` float(20,5) DEFAULT NULL,
  `rz_buy_three` float(20,5) DEFAULT NULL,
  `rz_repay_three` float(20,5) DEFAULT NULL,
  `rz_net_buy_three` float(20,5) DEFAULT NULL,
  `rq_sell_three` float(20,5) DEFAULT NULL,
  `rq_repay_three` float(20,5) DEFAULT NULL,
  `rq_net_sell_three` float(20,5) DEFAULT NULL,
  `rz_buy_five` float(20,5) DEFAULT NULL,
  `rz_repay_five` float(20,5) DEFAULT NULL,
  `rz_net_buy_five` float(20,5) DEFAULT NULL,
  `rq_sell_five` float(20,5) DEFAULT NULL,
  `rq_repay_five` float(20,5) DEFAULT NULL,
  `rq_net_sell_five` float(20,5) DEFAULT NULL,
  `rz_buy_ten` float(20,5) DEFAULT NULL,
  `rz_repay_ten` float(20,5) DEFAULT NULL,
  `rz_net_buy_ten` float(20,5) DEFAULT NULL,
  `rq_sell_ten` float(20,5) DEFAULT NULL,
  `rq_repay_ten` float(20,5) DEFAULT NULL,
  `rq_net_sell_ten` float(20,5) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_dx` (`hd_date`,`stock_code`)
) ENGINE=MyISAM AUTO_INCREMENT=3814 DEFAULT CHARSET=utf8 ;


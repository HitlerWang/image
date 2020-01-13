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
  `hd_date` varchar(15) NOT NULL,
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

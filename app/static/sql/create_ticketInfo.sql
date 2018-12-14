CREATE TABLE `ticketinfo` (
  `ticket_id` varchar(20) NOT NULL,
  `tel_phone` char(11) NOT NULL,
  `idcard_num` char(18) NOT NULL,
  `ticket_date` text,
  `start_from` text,
  `end_to` text,
  `train_number` text,
  `passengers` text NOT NULL,
  `passenger_num` int(11) NOT NULL,
  `success_rate` tinyint(4) NOT NULL,
  `price` float(8,2) NOT NULL DEFAULT '0.00',
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `seat_type` text,
  `is_student` tinyint(4) DEFAULT '0',
  `from_to` text,
  PRIMARY KEY (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


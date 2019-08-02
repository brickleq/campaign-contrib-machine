CREATE TABLE `census_data` (
  `id` int(11) NOT NULL,
  `zipcode_5` int(11) DEFAULT NULL,
  `pop_total` int(11) DEFAULT NULL,
  `unemployment_rate` double DEFAULT NULL,
  `median_household_income` double DEFAULT NULL,
  `healthcare_rate` double DEFAULT NULL,
  `hs_graduation_rate` double DEFAULT NULL,
  `assoc_degree_rate` double DEFAULT NULL,
  `bachelor_degree_rate` double DEFAULT NULL,
  `grad_degree_rate` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `zipcode_donations` (
  `id` int(11) NOT NULL,
  `zipcode_5` int(11) DEFAULT NULL,
  `CAND_PARTY` text,
  `donations_sum` double DEFAULT NULL,
  `donations_median` double DEFAULT NULL,
  `donations_count` int(11) DEFAULT NULL,
  `geometry` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
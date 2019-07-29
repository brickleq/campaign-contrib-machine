CREATE TABLE `candidate_committees` (
  `CAND_ID` varchar(9) DEFAULT NULL,
  `CAND_ELECTION_YR` int(4) DEFAULT NULL,
  `FEC_ELECTION_YR` int(4) DEFAULT NULL,
  `CMTE_ID` varchar(9) DEFAULT NULL,
  `CMTE_TP` varchar(1) DEFAULT NULL,
  `CMTE_DSGN` varchar(1) DEFAULT NULL,
  `LINKAGE_ID` int(12) NOT NULL,
  PRIMARY KEY (`LINKAGE_ID`)
);

CREATE TABLE `contributions` (
  `CMTE_ID` varchar(9) DEFAULT NULL,
  `TRANSACTION_PGI` varchar(5) DEFAULT NULL,
  `ZIP_CODE` varchar(9) DEFAULT NULL,
  `TRANSACTION_DT` varchar(8) DEFAULT NULL,
  `TRANSACTION_AMT` double(14,2) DEFAULT NULL,
  `SUB_ID` varchar(19) NOT NULL,
  `zipcode_5` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`SUB_ID`)
);
ALTER TABLE contributions ADD UNIQUE (SUB_ID);
CREATE TABLE `candidates` (
  `CAND_ID` varchar(9) NOT NULL,
  `CAND_NAME` varchar(200) DEFAULT NULL,
  `CAND_PTY_AFFILIATION` varchar(3) DEFAULT NULL,
  `CAND_ELECTION_YR` int(4) DEFAULT NULL,
  `CAND_OFFICE_ST` varchar(2) DEFAULT NULL,
  `CAND_OFFICE` varchar(1) DEFAULT NULL,
  `CAND_OFFICE_DISTRICT` varchar(2) DEFAULT NULL,
  `CAND_ICI` varchar(1) DEFAULT NULL,
  `CAND_STATUS` varchar(1) DEFAULT NULL,
  `CAND_PCC` varchar(9) DEFAULT NULL,
  `CAND_ST1` varchar(34) DEFAULT NULL,
  `CAND_ST2` varchar(34) DEFAULT NULL,
  `CAND_CITY` varchar(30) DEFAULT NULL,
  `CAND_ST` varchar(2) DEFAULT NULL,
  `CAND_ZIP` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`CAND_ID`)
);
ALTER TABLE candidates ADD UNIQUE (CAND_ID);
/*
mysqlimport  --ignore-lines=1 --fields-terminated-by=, --columns='CAND_ID,CAND_NAME,CAND_PTY_AFFILIATION,CAND_ELECTION_YR,CAND_OFFICE_ST,CAND_OFFICE,CAND_OFFICE_DISTRICT,CAND_ICI,CAND_STATUS,CAND_PCC,CAND_ST1,CAND_ST2,CAND_CITY,CAND_ST,CAND_ZIP' --local -u root -p campaign_contrib_machine_db contributions.csv 
*/


select * from candidates;
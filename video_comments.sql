SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for video_comments
-- ----------------------------
DROP TABLE IF EXISTS `video_comments`;
CREATE TABLE `video_comments` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL,
  `parent` int(20) NOT NULL DEFAULT '0',
  `reply` int(20) NOT NULL DEFAULT '0',
  `content` longtext NOT NULL,
  `create_time` datetime NOT NULL,
  `vid` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_fk` (`uid`),
  KEY `video_fk` (`vid`),
  CONSTRAINT `user_fk` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `video_fk` FOREIGN KEY (`vid`) REFERENCES `video_detail` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

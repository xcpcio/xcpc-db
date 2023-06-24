import mysql.connector
import unicodedata
from competition_result import Result

class XCPCRatingDataConnector:
    dataSource = None

    def __init__(self, address, port, user, password):
        self.dataSource = mysql.connector.connect(host = address, port = port, user = user, password = password, database = "xcpc")
    
    def __del__(self):
        if self.dataSource != None:
            self.dataSource.close()

    def __standardName(self, name):
        # 标准化所有名字的函数
        # strip
        ret = name.strip()
        # 中文标点全部转为英文标点
        ret = unicodedata.normalize('NFKC', ret)
        return ret
    
    def __queryOneResult(self, sql):
        try:
            queryCursor = self.dataSource.cursor(buffered = True)
            queryCursor.execute(sql)
            res = queryCursor.fetchone()
            ret = res
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            ret = None
        finally:
            queryCursor.close()
            return ret
    
    def __insert(self, sql):
        try:
            queryCursor = self.dataSource.cursor()
            queryCursor.execute(sql)
            self.dataSource.commit()
            ret = queryCursor.lastrowid
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            ret = None
        finally:
            queryCursor.close()
            return ret
    
    # 获得学校 id。如果没有，会返回一个 -1。
    def findSchool(self, name):
        name = self.__standardName(name)
        sql = "SELECT id FROM schools WHERE name = \"%s\"" % name
        res = self.__queryOneResult(sql)
        if res == None:
            ret = -1
        else:
            ret = res[0]
        return ret
    
    def insertSchool(self, name):
        name = self.__standardName(name)
        sql = "INSERT INTO schools (name) VALUES (\"%s\")" % name
        return self.__insert(sql)
    
    # build team members str
    def __getTeamMembersStr(self, members):
        team_members = []
        team_members_str = ""
        for x in members:
            team_members.append(self.__standardName(x))
        team_members.sort()
        for x in team_members:
            team_members_str += x
        return team_members_str
    
    def __validateCompetition(self, competition_id):
        comp = self.getCompetition(competition_id)
        if comp == None:
            raise Exception(
                "No competition with id %d exists. Be sure to create the competition before inserting results of it." % competition_id)

    # 获得一个学校某个指定队员组成的队伍编号。队员用一个可以被遍历的玩意儿塞进来就行，别的不需要处理了，交由这个函数统一处理
    # 返回单个id，因为默认三个人名一样、在一个学校的一个队只会有特么的唯一一个id
    # 如果以后有变化再说吧（紫鲨了
    def findTeam(self, school_id, members):
        team_members_str = self.__getTeamMembersStr(members)
        sql = "SELECT id FROM teams WHERE school_id = %d and team_members_str = \"%s\"" % (school_id, team_members_str)
        res = self.__queryOneResult(sql)
        if res == None:
            ret = -1
        else:
            ret = res[0]
        return ret
    
    def getTeam(self, team_id):
        sql = "SELECT * FROM teams WHERE id = %d" % (team_id)
        return self.__queryOneResult(sql)
    
    def insertTeam(self, school_id, name, members):
        team_members_str = self.__getTeamMembersStr(members)
        sql = "INSERT INTO teams (school_id, name, team_members_str) VALUES (%d, \"%s\", \"%s\")" % (school_id, name, team_members_str)
        res = self.__insert(sql)
        if res == None:
            print("爆炸了兄弟！")
            return None
        for x in members:
            x = self.__standardName(x)
            sql = "INSERT INTO competitors (name) VALUES (\"%s\")" % (x)
            competitor_id = self.__insert(sql)
            sql = "INSERT INTO teams_competitors (team_id, competitor_id) VALUES (%d, %d)" % (res, competitor_id)
            self.__insert(sql)
        return res
    
    def getCompetition(self, competition_id):
        sql = "SELECT * FROM competitions WHERE id = %d" % (competition_id)
        return self.__queryOneResult(sql)
    
    def insertCompetition(self, year, type, name):
        sql = "INSERT INTO competitions (year, type, name) VALUES (%d, %d, \"%s\")" % (year, type, name)
        return self.__insert(sql)
    
    def insertResult(self, competition_id, team_id, rank, is_official, school_rank, prize):
        if school_rank == None:
            school_rank = -1
        if prize == None:
            prize = "未知"
        if is_official:
            is_official = 1
        else:
            is_official = 0
        sql = "INSERT INTO results (competition_id, team_id, rank, school_rank, prize, is_official) VALUES (%d, %d, %d, %d, \"%s\", %d)" % (competition_id, team_id, rank, school_rank, prize, is_official)
        return self.__insert(sql)
    
    def addResult(self, school, team_name, members, competition_id, rank, is_official, school_rank = None, prize = None, validate = True):
        # 最终超级导入函数
        # 我也不知道会发生什么……
        
        # get school
        school_id = self.findSchool(school)
        if school_id == -1:
            school_id = self.insertSchool(school)
        
        # try to find teams
        team_id = self.findTeam(school_id, members)
        if team_id == -1:
            team_id = self.insertTeam(school_id, team_name, members)

        if validate:
            self.__validateCompetition(competition_id)
        
        # 考虑到一般来说competition_id 都不会去找，就自己填吧
        
        return self.insertResult(competition_id, team_id, rank, is_official, school_rank, prize)
        
    def importResult(self, result, validate = True):
        # 最终超级导入函数 wrapper
        return self.addResult(result.school, result.team_name, result.members, result.competition_id, result.rank, result.is_official, result.school_rank, result.prize, validate)

    def importResultBatch(self, results):
        competition_id = results[0].competition_id
        if competition_id == None:
            raise Exception("Competition id not provided!")
        
        for x in results:
            if x.competition_id != competition_id:
                raise Exception("Competition id not match!")
            
        self.__validateCompetition(competition_id)
        # 批量导入
        for x in results:
            print(self.importResult(x, validate = False))
        
test = XCPCRatingDataConnector("sh-cynosdbmysql-grp-51uynye4.sql.tencentcdb.com", 22347, "root", "f70v655V9kMv0j2jUz")
#print(test.findSchool("测试学校"))
#print(test.findSchool("不存在的学校"))
#print(test.getTeam(1))
#print(test.findTeam(1, ["倪昊斌", "刘严培", "黄文瀚"]))
#print(test.insertTeam(1, "测试队伍", ["黄文瀚", "倪昊斌", "刘严培"]))
#print(test.insertSchool("测试学校"))
#print(test.insertCompetition(1999, 1, "测试比赛"))
print(test.addResult("测试学校", "测试队伍", ["倪昊斌", "刘严培", "黄文瀚"], 1, 1, True, 1, "超级冠军"))
test.importResultBatch([
    Result("测试学校", "测试队伍", ["倪昊斌", "刘严培", "黄文瀚"], 1, 1, True, 1, "超级冠军"),
    Result("测试学校", "测试队伍", ["倪昊斌", "刘严培", "黄文瀚"], 1, 1, True, 1, "超级冠军"),
    Result("测试学校", "测试队伍", ["倪昊斌", "刘严培", "黄文瀚"], 1, 1, True, 1, "超级冠军")])

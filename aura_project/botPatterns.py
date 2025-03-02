class botPatterns:
	preprocess = [("(WHAT|HOW|WHY|WHERE|IT|DO|WHEN|THERE|THAT|HE|SHE)'?(s|z)", "\\1 IS"),
			("YOU'RE", "YOU ARE"), ("I'M", "I AM"), ("I'VE", "I HAVE"), ("\+", "PLUS"), ("\*", "INTO"), ("/", "BY"), ("([0-9])\s*-", "\\1 MINUS")
		]
	taggrammar = [
		(r'(?i)^(pls|please|plz)$', 'REQUEST'),
		(r'(?i)^(me|i|my|mine|our|us|we)$', 'PERSONFST'),
		(r'(?i)^(you|yours?|u|ur)$', 'PERSONSCND'),
		(r'(?i)^(want|would)$', 'INTENTION'),
		(r'(?i)^(hey|hi|hello)$', 'GREETINGS'),
		(r'(?i)^(pain|paining|pained|pains|hurt|hurting|hurts|ache)$', 'PROB'),
		(r'(?i)^(the|an|a)$', 'ARTICLES'),
		(r'(?i)^(tv|television|monitor|screen)$', 'TVST'),
		(r'(?i)^(movie|movies|videos|video)$', 'VIDST'),
		(r'(?i)^(can|could|ask|should)$', 'ASK'),
		(r'^[1-1000000000]$', 'NUM'),
		(r'^(?i)(hm)+$', 'HM'),
		(r'^(?i)(mm)+$', 'MM'),
		(r'(?i)^(am|are|r|is|were|be|being|been|have|has|had|shall|will|do|does|did|must might|could|would|should)$', 'HELPINGVERBS'),
		(r'(?i)^(.+)$', 'SELFTAG')
	    ]
	chunkgrammar = r'''
			NXMED:
				{<.*>*<WHEN><HELPINGVERBS>(<PERSONFST>|<ARTICLES>)<NEXT>?<UPCOMING>?(<MEDICINE>|<MEDICATION>|<MEDICINES>)<REMAINDER>?<REMINDER>?<.*>*}
				{<.*>*<WHEN><ASK><PERSONFST><TAKE><PERSONFST>?<ARTICLES>?<NEXT>?<UPCOMING>?(<MEDICINE>|<MEDICATION>|<MEDICINES>)<.*>*}
				{<.*>+(<NEXT>|<UPCOMING>)?(<MEDICINES>|<MEDICINE>|<MEDICATION>)<.*>*}
                    WHEREBOT:
                            {<.*>*<WHERE><HELPINGVERBS><PERSONSCND><NOW>?<.*>*}
		    WHATIS:
			    {<GREETINGS>?<WHAT><HELPINGVERBS>}
            CSORRY:
                {<.*>*(<SORRY>|<FORGIVE>|<FORGIVENESS>|<FORGIVING>)<.*>*}
		    LAUGH:
			    {<GREETINGS>?<HA>+}
            ANGRYATBOT:
                            {<.*>*(<IDIOT>|<STUPID>|<MAD>|<GOOD><FOR><NOTHING>|<ANNOYING>|<DISTURBING>|<BORING>|<BAD>|<FIRED>|<GET><LOST>)<.*>*}
                
            CANASKQUEST:
                            {<GREETINGS>?<ASK><PERSONFST><ASK><PERSONSCND><ARTICLES>?(<QUESTION>|<SOMETHING>)}
                            {<GREETINGS>?<ANSWER><PERSONFST><QUESTION>}
            BOTSMARTER:
                            {<GREETINGS>?<ASK><PERSONSCND><GET><SMARTER>}
                            {<GREETINGS>?<ASK><PERSONSCND><BECOME><SMARTER>}
		    CWHOBOT:
			    {<GREETINGS>?(<WHO>|<WHAT>)<HELPINGVERBS><PERSONSCND>}
			    {<GREETINGS>?<WHATIS><PERSONSCND><NAME>}
			    {<GREETINGS>?<NAME><REQUEST>}
		    PRAISE:
			    {<GREETINGS>?((<GOOD>|<GREAT>)(<JOB>|<WORK>)?|<KEEP><IT><UP>|<EXELLENT>|<PERSONSCND><HELPINGVERBS><VERY>?(<INTELIGENT>|<GOOD>|<SMART>|<GREAT>))}
                            {<GREETINGS>?<PERSONSCND><HELPINGVERBS><VERY>?(<PRETTY>|<BEAUTIFUL>)}
                            {<GREETINGS>?<PERSONSCND><LOOK><VERY>?<GOOD>}
                            {<GREETINGS>?<PERSONSCND><HELPINGVERBS><ARICLES>?<SO>?<VERY>?(<CLEVER>|<SMART>|<CRAZY>|<FUNNY>|<GOOD>)}
                            
		    THANK:
			    {<.*>*(<THANKS>|<THANK><PERSONSCND>)<.*>*}
		    CWELCOME:
                            {<.*>*<PERSONSCND><HELPINGVERBS><WELCOME><.*>}
                            {<.*>*<WELCOME><.*>*}
		    CAREBOT:
			    {<GREETINGS>?<HELPINGVERBS><PERSONSCND><ARTICLES>(<BOT>|<ROBOT>|<CHATBOT>)}
                            {<GREETINGS>?<PERSONSCND><HELPINGVERBS><ARTICLES>(<BOT>|<ROBOT>|<CHATBOT>)}
                    BOTBUSY:
                            {<GREETINGS>?<HELPINGVERBS><PERSONSCND><BUSY>}
		    AGE:
			    {<GREETINGS>?<HOW><OLD><HELPINGVERBS><PERSONSCND>}
			    {<GREETINGS>?<WHATIS><PERSONSCND><AGE>} 
                            {<GREETINGS>?<WHATIS><PERSONSCND><BIRTH><DATE>}
                            {<GREETINGS>?<WHEN><HELPINGVERBS><PERSONSCND><BORN>}
		    CWHATBOTDO:
			    {<GREETINGS>?<WHATIS><ALL>?<ASK>?<PERSONSCND><HELPINGVERBS>}
			    {<GREETINGS>?<WHAT><ALL>?<ASK>?<PERSONSCND><HELPINGVERBS>}
                            {<GREETINGS>?<PERSONFST><HELPINGVERBS><BORED>}
			    {<GREETINGS>?<HOW><ASK><PERSONSCND><HELP><PERSONFST>}
                            {<GREETINGS>?<ASK><PERSONSCND><HELP><PERSONFST>}
                            {<.*>*<PERSONFST><NEED><.*>*<HELP><.*>*}

		    CALCULATE:
			    {<GREETINGS>?<NUM><(\+|-|\*|\/)><NUM>}
                    EMERGENCY:
                            {<.*>*<PROB><.*>*}
		    DATE:
			    {<GREETINGS>?<WHATIS><ARTICLES>?<DATE><TODAY>?}
			    {<GREETINGS>?<DATE>}
			    {<GREETINGS>?<WHATIS><DATE><TODAY>}
			    {<GREETINGS>?<WHATIS><DAY><TODAY>}
			    {<GREETINGS>?<WHATIS><TODAY><IS><DATE>}
			    {<GREETINGS>?<TODAY><IS><DAY>}
		    TIME:
			    {<GREETINGS>?<WHATIS><ARTICLES>?<TIME>}
			    {<GREETINGS>?<TIME>}
		    WEATHER:
			    {<GREETINGS>?<HOW|WHATIS><HELPINGVERBS>?<ARTICLES>?<WEATHER|TEMPERATURE>}
			    {<GREETINGS>?(<WEATHER>|<TEMPERATURE>)}
		    HOWRU:
			    {<GREETINGS>?<HOW><HELPINGVERBS><PERSONSCND>}
			    {<GREETINGS>?<HOWDY>}
		    WHATSUP:
			    {<GREETINGS>?<WHATIS><UP>}
			    {<GREETINGS>?<SUP>}
			    {<GREETINGS>?<WHATIS><GOING><ON>}
                            {<GREETINGS>?<WHATIS><PERSONSCND><DOING>}
		    TBTPLAY: 
			    {<GREETINGS>?<ASK>?<PERSONSCND>?<REQUEST>?<PLAY><FOR>?<PERSONFST>?<SONGS?>?<MUSIC>?<THE>?}
			    {<GREETINGS>?<ASK>?<PERSONSCND>?<REQUEST>?<PLAY>?<FOR>?<PERSONFST>?<SONGS?>?<MUSIC><THE>?}
			    {<GREETINGS>?<PERSONFST>?(<ITENTION><LIKE><TO>)?<WANNA>?(<WANT><TO>)?<LISTEN><TO>?<SONGS?>?<MUSIC>?}
		    DEFINATIONS:
			    {<GREETINGS>?<WHATIS><.+>}
			    {<GREETINGS>?(<WHO>|<WHY>|<WHERE>|<WHEN>)<HELPINGVERBS><.+>}
			    {<GREETINGS>?<DEFINE><.+>}
			    {<GREETINGS>?<TELL><PERSONFST>(<ALL>|<ABOUT>|<ALL ABOUT>)<.+>}
		    CMDPLAYNEWS:
                            {<.*>*<NEWS><.*>*}
			    {<GREETINGS>?<TBTPLAY>?<NEWS>}
			    {<GREETINGS>?<CURRENT><AFFAIRS>}
		    GREET:
			    {^<GREETINGS>}
			    {<GREETINGS>?<PERSONFST><NAME><HELPINGVERBS>?<.*>}
			    {<GREETINGS>?<PERSONFST><HELPINGVERBS><.+>}
		    CREATOR:
			    {<GREETINGS>?<WHO>(<CREATED>|<MADE>)<PERSONSCND>}
			    {<GREETINGS>?<WHO><HELPINGVERBS><PERSONSCND><CREATOR>}
                            {<WHO><HELPINGVERBS><PERSONSCND><BOSS>}
		BEFRIEND:
			{<GREETINGS>?<ASK><PERSONFST><HELPINGVERBS><FRIENDS>}
			{<GREETINGS>?<HELPINGVERBS><PERSONSCND><HELPINGVERBS><PERSONFST><FRIEND>}
			{<GREETINGS>?<HELPINGVERBS><PERSONFST><FRIENDS>}
                CSODOI:
                        {<.*>*(<HATE>|<LOVE>)<.*>*}
		OK:
			{<GREETINGS>?<OK>}
			{<GREETINGS>?<HM>}
			{<GREETINGS>?<MM>}
			{<GREETINGS>?<FINE>}
		CMDPLAYONTV:
			{<GREETINGS>?<TBTPLAY><.*>*<VIDST><TVST>?}
		NNP: 
			{<(?!THAN|CSORRY|NXMED|CSODOI|WHEREBOT|EMERGENCY|AGE|BOTSMARTER|CANASKQUEST|CMDPLAYONTV|BOTBUSY|LAUGH|PRAISE|CWELCOME|BEFRIEND|CWHOBOT|CREATOR|OK|TBT|NEWS|DEF|GRE|TIM|WEATHER|HOWRU|CMD|GREET|CWHATBOTDO|CAREBOT|WHATSUP|DA|ANGRY).*>+}
		CMDPLAYSONG:
			{<GREETINGS>?<TBTPLAY><NNP>}
'''



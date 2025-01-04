from datetime import datetime
from typing import Literal

import pandas
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pandas import DataFrame
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback


class ReportDetected(BaseModel):
    direction: Literal['to_estonia', 'to_russia']
    came_to_border_at: datetime | None = None
    first_country_checkpoint_entered: datetime | None = None
    first_country_checkpoint_exit: datetime | None
    second_country_checkpoint_entered: datetime | None
    second_country_checkpoint_exit: datetime | None
    comment: str | None


class ChatMessage(BaseModel):
    report_detected: ReportDetected | None


load_dotenv()
model = ChatOpenAI(model_name="gpt-4o", temperature=0)
parser = PydanticOutputParser(pydantic_object=ChatMessage)
prompt = ChatPromptTemplate(messages=[SystemMessage('You must read a message and fill out fields. If there is no report detected return None for the report detected field in the message.\n '
                                           '`first_country_checkpoint_entered` and `second_country_checkpoint_exit` ARE ALWAYS REQUIRED to be SET TO APPROPRIATE DATETIME!!! THAT IS BASICALLY START AND END OF BORDER PASSING!\n'+parser.get_format_instructions()),
                             # HumanMessage('Отчет- 20.09- приехали в Нарву на электричке в 13:30, очереди не было, сразу зашли на границу- в итоге эстонскаяи русская в сумме 25 минут! @@@ 2024-09-20 12:07:18'),
                             # AIMessage('{"report_detected": {"direction": "to_russia", "came_to_border_at": "2024-09-20T13:30:00", "first_country_checkpoint_entered": "2024-09-20T13:30:00", "first_country_checkpoint_exit": null, "second_country_checkpoint_entered": null, "second_country_checkpoint_exit": "2024-09-20T13:55:00", "comment": "Очереди не было, сразу зашли на границу"}}'),
                             # HumanMessage('Отчет о прохождении границы 20.09. Люкс выехал в 8:45 из спб. В 11:30 были на границе. В 12:10 вышли в Нарве. Ждём пару человек в автобусе. У наших чемоданы на ленту. Эстонцы не смотрели. У кого то выборочно. Эстонцы спросили куда едете. Сказали, что другая страна Евросоюза. Проходили с паспортом Израиля. Просили документы на отель или адрес проживания (если едете к знакомым) и обратный билет.  Всем удачи 🙏 @@@ 2024-09-20 09:54:42'),
                             # AIMessage('{"report_detected": {"direction": "to_estonia", "came_to_border_at": null, "first_country_checkpoint_entered": "2024-09-20T11:30:00", "first_country_checkpoint_exit": null, "second_country_checkpoint_entered": null, "second_country_checkpoint_exit": "2024-09-20T12:10:00", "comment": "Ждём пару человек в автобусе. У наших чемоданы на ленту. Эстонцы не смотрели. У кого то выборочно. Эстонцы спросили куда едете. Сказали, что другая страна Евросоюза. Проходили с паспортом Израиля. Просили документы на отель или адрес проживания (если едете к знакомым) и обратный билет."}}'),
                             # HumanMessage('Отчет в копилку:  В воскресение в 14:10 встала в очередь в Нарве. В 16:40 вышла в Ивангороде.  Час провела на эстонской границе, остальное время в парнике.  Минут 5 провела у окошка таксфри.  Таможенники Эстонии открыли багаж, спросили о наличии новых товаров дороже 300€, проштамповали чеки таксфри и отпустили с миром.  Таможня в России только стандартные вопросы везу ли что-то запрещенное и денег больше 10к$  Пограничник Эстонии, долго допрашивал про все документы и где живу. И основания наличия документов. И про наличные €.  Пограничница России - молча пропустила. @@@ 2024-09-17 10:23:50'),
                             # AIMessage('{"report_detected": {"direction": "to_russia", "came_to_border_at": "2024-09-15T14:10:00", "first_country_checkpoint_entered": null, "first_country_checkpoint_exit": null, "second_country_checkpoint_entered": null, "second_country_checkpoint_exit": "2024-09-15T16:40:00", "comment": "Час провела на эстонской границе, остальное время в парнике. Минут 5 провела у окошка таксфри. Таможенники Эстонии открыли багаж, спросили о наличии новых товаров дороже 300€, проштамповали чеки таксфри и отпустили с миром. Таможня в России только стандартные вопросы везу ли что-то запрещенное и денег больше 10к$. Пограничник Эстонии, долго допрашивал про все документы и где живу. И основания наличия документов. И про наличные €."}}'),
                             # HumanMessage('Отчет:  16.09.24 Из Таллинна до Нарвы автобусом ( местным Люксом) на 8.15. Спасибо водителю, что взял наших легавых в салон по билетам ( наличие намордника обязательно! По правилам должны быть в переноске, но такие размеры не влезут) В 11.40 встали напротив таксистов. В 14.15 внутрь эст КПП запустили. Досмотр чемодана, вопросы про наличие €  С российской вышли в 15.50. Долго оформляли декларации и ждали ветеринара. Так же очередь задерживали несуны, со своими объяснительными.  С России, в это время, очереди вообще не было. @@@ 2024-09-16 20:31:20'),
                             # AIMessage('{"report_detected": {"direction": "to_estonia", "came_to_border_at": "2024-09-16T11:40:00", "first_country_checkpoint_entered": "2024-09-16T14:15:00", "first_country_checkpoint_exit": null, "second_country_checkpoint_entered": null, "second_country_checkpoint_exit": "2024-09-16T15:50:00", "comment": "Спасибо водителю, что взял наших легавых в салон по билетам ( наличие намордника обязательно! По правилам должны быть в переноске, но такие размеры не влезут) В 11.40 встали напротив таксистов. Долго оформляли декларации и ждали ветеринара. Так же очередь задерживали несуны, со своими объяснительными. С России, в это время, очереди вообще не было."}}'),
                             HumanMessage('Вчера было много отчетов в чате. @@@ 2024-09-16 09:21:36'),
                             AIMessage('{"report_detected": null}'),
                             HumanMessage('отчет 10.10. Нарва-Ивангород - встала в очередь в 11:15 - зашла на нарвское кпп в 18:15 - зашла на кпп рф в 18:35 - вышла в ивангород в 18:45 @@@ 2024-10-11 07:18:35'),
                             AIMessage('{"report_detected": {"direction": "to_russia", "came_to_border_at": "2024-10-10T11:15:00", "first_country_checkpoint_entered": "2024-10-10T18:15:00", "first_country_checkpoint_exit": null, "second_country_checkpoint_entered": "2024-10-10T18:35:00", "second_country_checkpoint_exit": "2024-10-10T18:45:00", "comment": null}}'),
                             # HumanMessage('Отчет за сегодня,кому интересно.Выехали из Питера на маршрутке от м.Проспект Ветеранов в 8.20.На границе в  Ивангороде были в 10.20.Очередь ровно 10 человек,в основном наша маршрутка.Простояли пару минут и границу закрыли .74 летний мужчина упал прямо в рамке контроля.Сотрудники вызвали скорую.Пока скорая ехала,он умер.Скорая зафиксировала смерть.Потом его накрыли черным пластиковым пакетом и снова стали пропускать людей.В общей сложности простояли минут 40.Людей пропускали с другой строны,не через рамку.В рамке лежал труп.На Эстонской строне со стороны России не было никого.Прошли за 1 минуту через автоматические ворота.Досмотра вещей тоже не было.Очередь со стороны Нарвы в Россию очень длинная,конца даже не видно.Стоящие в ней люди сказали,что у  эстонцев сбой в системе и уже очень долго никого не запускают.Вот такой сегодня треш.Женщины в очереди сказали,что мужчине было 74 года,он эстонец из несунов. @@@ 2024-10-11 11:01:18'),
                             # AIMessage('{"report_detected": {"direction": "to_estonia", "came_to_border_at": "2024-10-11T10:20:00", "first_country_checkpoint_entered": null, "first_country_checkpoint_exit": null, "second_country_checkpoint_entered": null, "second_country_checkpoint_exit": "2024-10-11T11:00:00", "comment": "Выехали из Питера на маршрутке от м.Проспект Ветеранов, Прошли за 1 минуту через автоматические ворота. Досмотра вещей тоже не было. Очередь со стороны Нарвы в Россию очень длинная, конца даже не видно."}}'),
                             SystemMessage('NOW START! Here is the message for you to process:'),
                             MessagesPlaceholder('messages')
                             ])
df = pandas.read_csv('parsed_messages.csv')
with get_openai_callback() as cb:
    result_df = []
    for index, row in df.iterrows():
        text = row['text']

        if text:
            print(text)
            prompt_and_model = prompt | model
            output = prompt_and_model.invoke(dict(messages=[HumanMessage(f"{text} @@@ {row['date']}")]))
            report_parsed = parser.invoke(output)
            if not report_parsed.report_detected:
                continue
            print(report_parsed)
            result_df.append(report_parsed.model_dump()['report_detected'])
            DataFrame(result_df).to_csv('reports.csv')
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")

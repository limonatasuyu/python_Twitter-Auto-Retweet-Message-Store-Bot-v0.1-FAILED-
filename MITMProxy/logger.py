import datetime
import os


def get_base_path():
    module_path = os.path.abspath(__file__)
    module_directory = os.path.dirname(module_path)
    base_path = os.path.join(module_directory, '../logs/interceptor')
    return base_path


def get_file_path(file_name):
    current_day = datetime.datetime.now().strftime("%Y-%m-%d")
    base_path = get_base_path()
    folder_path = os.path.join(base_path, current_day)
    return os.path.join(folder_path, f"{file_name}.txt")


class Logger:
    is_new_session = True
    is_session_started = False
    info_path = get_file_path("info")
    was_folders_created = os.path.exists(get_file_path("info"))

    def __init__(self):
        self.valid_data_types = ["raw_content", "content", "text", "url", "method", "headers", "status_code"]
        self.current_day = datetime.datetime.now().strftime("%Y-%m-%d")
        self.base_path = get_base_path()
        self.folder_path = os.path.join(self.base_path, self.current_day)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def get_file_path(self, file_name):
        return os.path.join(self.folder_path, f"{file_name}.txt")

    def add_blank_line(self, file_path):
        with open(file_path, 'a') as file:
            file.write("\n")

    def add_blank_lines_to_all_logs(self):
        for data_type in self.valid_data_types + ["all_logs"]:
            file_path = self.get_file_path(data_type)
            self.add_blank_line(file_path)

    def log(self, theData, data_type, log_type="data"):
        if log_type not in ["data", "text"]:
            raise ValueError(f"log_type should either be 'data': string (default) or 'text': string. Not `{log_type}`, which have {type(log_type)} type")

        if not Logger.is_session_started:
            current_date = str(datetime.datetime.now())
            self.__log_text(f"SESSION FOR {current_date} STARTING")
            Logger.is_session_started = True

        if log_type == "text" and data_type == "text":
            self.__log_text(theData)
            return
        self.__log_data(theData, data_type)

    def __log_text(self, text):
        current_time = datetime.datetime.now().strftime("%H-%M-%S")
        log_line = f"[{current_time}] {text}"
        info_file_path = self.get_file_path("info")
        with open(info_file_path, "a") as info_file:
            info_file.write(log_line)
            self.add_blank_line(info_file_path)

    def __log_data(self, data, data_type):
        if data_type not in self.valid_data_types:
            raise ValueError(f"Invalid data type: {data_type}, which have type {type(data_type)}")

        if Logger.was_folders_created:
            self.check_and_create_new_folder()

        current_time = datetime.datetime.now().strftime("%H-%M-%S")
        log_line = f"[{current_time}] {data}"

        data_type_specific_logs_path = self.get_file_path(data_type)
        with open(data_type_specific_logs_path, 'a') as file:
            file.write(log_line)
            self.add_blank_line(data_type_specific_logs_path)

        # Include "all_logs.txt"
        all_logs_path = self.get_file_path("all_logs")
        with open(all_logs_path, 'a') as file_all_logs:
            file_all_logs.write(log_line)
            self.add_blank_line(all_logs_path)

        # Include "url" and "method" logs in all other logs
        if data_type in ["url", "method", "status_code"]:
            for valid_data_type in self.valid_data_types:
                if valid_data_type != data_type:
                    other_logs_path = self.get_file_path(valid_data_type)
                    with open(other_logs_path, 'a') as file_other_logs:
                        file_other_logs.write(log_line)
                        self.add_blank_line(other_logs_path)

        self.check_and_create_new_folder()

    def check_and_create_new_folder(self):
        if not Logger.is_new_session:
            return
        info_path = self.get_file_path("info")
        with open(info_path, 'r') as methods_file:
            lines = methods_file.readlines()
            new_folder_name = lines[1].strip().split("]")[0][1:].replace(":", "-")

            stored_logs_path = os.path.join(self.base_path, f"{self.current_day}/stored_logs")
            new_folder_path = os.path.join(stored_logs_path, new_folder_name)
            os.makedirs(new_folder_path, exist_ok=True)

            # Move the current logs to the new folder
            for data_type in self.valid_data_types + ["all_logs", "info"]:
                current_file_path = self.get_file_path(data_type)
                new_file_path = os.path.join(new_folder_path, f"{data_type}.txt")
                os.rename(current_file_path, new_file_path)
            Logger.was_folders_created = True
            Logger.is_new_session = False

    def log_flow(self, flow):
        raw_content = flow.response.raw_content
        content = ""
        text = ""

        try:
            content = flow.response.content
        except ValueError as e:
            print(f"Error while trying to get flow.response.content from url {flow.request.url}: {str(e)[:200]}")

        content_type = ""
        if "content-type" in flow.response.headers:
            content_type = flow.response.headers["content-type"].lower()

        content_types = ["text", "html", "json", "xml", "plain", "javascript", "css", "utf-8"]
        if content_type == "":
            text = "NO DATA TO SHOW AS TEXT FROM NO CONTENT TYPE"
        elif any(content_type.endswith(ct) for ct in content_types) or any(content_type.startswith(ct) for ct in content_types):
            try:
                text = flow.response.text
            except UnicodeDecodeError as e:
                print(f"Error decoding response text: {str(e)[:200]}")
            except Exception as e:
                print(f"Unindentified error while decodig response text: {str(e)[:200]}")
                text = f"NO DATA TO SHOW AS TEXT FROM CONTENT TYPE {content_type}"

        else:
            text = f"NO DATA TO SHOW AS TEXT FROM CONTENT TYPE {content_type}"

        self.log(f"[URL] {flow.request.url}", "url")
        self.log(f"[METHOD] {flow.request.method}", "method")
        self.log(f"[REQUEST]  [HEADERS] {flow.request.headers}", "headers")
        self.log(f"[RESPONSE] [HEADERS] {flow.response.headers}", "headers")
        self.log(f"[STATUS CODE] {flow.response.status_code}", "status_code")

        if flow.request.method in ["POST", "PUT", "PATCH", "DELETE", "OPTIONS", "PROPFIND", "PROPPATCH"]:
            request_raw_content = flow.request.raw_content
            request_content = ""
            request_text = ""

            try:
                request_content = flow.request.content
            except ValueError as e:
                print(f"Error while trying to get flow.request.content from url {flow.request.url}: {str(e)[:200]}")
            try:
                request_text = flow.request.text
            except ValueError as e:
                print(f"Error while trying to get flow.request.text from url {flow.request.url}: {str(e)[:200]}")

            self.log(f"[REQUEST] [RAW CONTENT] {request_raw_content}", "raw_content")
            self.log(f"[REQUEST] [CONTENT] {request_content}", "content")
            self.log(f"[REQUEST] [TEXT] {request_text}", "text")

        self.log(f"[RESPONSE] [RAW CONTENT] {raw_content}", "raw_content")
        self.log(f"[RESPONSE] [CONTENT] {content}", "content")
        self.log(f"[RESPONSE] [TEXT] {text}", "text")
        self.add_blank_lines_to_all_logs()

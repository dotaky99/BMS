import datetime
import sqlite3
from datetime import timedelta
import win32crypt
from Cryptodome.Cipher import AES
import json
import os
import Database
from BrowserParse import CacheParser


def Browser_parser():
    source1=sqlite3.connect("COPY\\BROWSER\\History")
    source2 = sqlite3.connect("COPY\\BROWSER\\Web Data")
    source3 = sqlite3.connect("COPY\\BROWSER\\Cookies")
    source4 = sqlite3.connect("COPY\\BROWSER\\Login Data")
    s_cur1 = source1.cursor() #url, keyword
    s_cur2 = source2.cursor() #autofill 파싱
    s_cur3 = source3.cursor() #쿠키 파싱
    s_cur4 = source4.cursor() #login 파싱
    s_cur5 = source1.cursor() #download Parsing

    url_data_list=[]
    url_data_list_2=[]
    download_data_list = []
    download_data_list_2 = []
    keyword_data_list = []
    keyword_data_list_2 = []
    autofill_data_list = []
    autofill_data_list_2 = []
    bookmark_data_list = []
    bookmark_data_list_2 = []
    cookie_data_list = []
    cookie_data_list_2 = []
    login_data_list = []
    login_data_list_2 = []
    pref_data_list = []
    pref_data_list_2 = []
    cloud_data_list = []
    cloud_data_list_2 = []


    def change_last_modified_time(str):
        before_change = str.split(' ', maxsplit=6)
        month = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
        }

        if before_change[2] in list(month.keys()):
            time_friendly = month[before_change[2]]
        elif before_change[2] is None:
            time_friendly = None
        else:
            time_friendly = '[Error - Unknown Danger Code]'

        after_change = before_change[3] + "-" + time_friendly + "-" + before_change[1] + " " + before_change[4]

        # return timestamp
        return after_change

    def to_datetime(timestamp, timezone=None):
        """Convert a variety of timestamp formats to a datetime object."""

        try:
            if isinstance(timestamp, datetime.datetime):
                return timestamp
            try:
                timestamp = float(timestamp)
            except:
                timestamp = 0

            if 13700000000000000 > timestamp > 12000000000000000:  # 2035 > ts > 1981
                # Webkit
                new_timestamp = datetime.datetime.utcfromtimestamp((float(timestamp) / 1000000) - 11644473600)
            elif 1900000000000 > timestamp > 2000000000:  # 2030 > ts > 1970
                # Epoch milliseconds
                new_timestamp = datetime.datetime.utcfromtimestamp(float(timestamp) / 1000)
            elif 1900000000 > timestamp >= 0:  # 2030 > ts > 1970
                # Epoch
                new_timestamp = datetime.datetime.utcfromtimestamp(float(timestamp))
            else:
                new_timestamp = datetime.datetime.utcfromtimestamp(0)

            if timezone is not None:
                try:
                    return new_timestamp.replace(tzinfo=pytz.utc).astimezone(timezone)
                except NameError:
                    return new_timestamp
            else:
                return new_timestamp
        except Exception as e:
            print(e)

    def friendly_date(timestamp):
        if isinstance(timestamp, (str, int)):
            return to_datetime(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        elif timestamp is None:
            return ''
        else:
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def decode_transition(transition):
        # Source: http://src.chromium.org/svn/trunk/src/content/public/common/page_transition_types_list.h
        transition_friendly = {
            0: 'link',  # User got to this page by clicking a link on another page.
            1: 'typed',  # User got this page by typing the URL in the URL bar.  This should not be
            #  used for cases where the user selected a choice that didn't look at all
            #  like a URL; see GENERATED below.
            # We also use this for other 'explicit' navigation actions.
            2: 'auto bookmark',  # User got to this page through a suggestion in the UI, for example)
            #  through the destinations page.
            3: 'auto subframe',  # This is a subframe navigation. This is any content that is automatically
            #  loaded in a non-toplevel frame. For example, if a page consists of
            #  several frames containing ads, those ad URLs will have this transition
            #  type. The user may not even realize the content in these pages is a
            #  separate frame, so may not care about the URL (see MANUAL below).
            4: 'manual subframe',  # For subframe navigations that are explicitly requested by the user and
            #  generate new navigation entries in the back/forward list. These are
            #  probably more important than frames that were automatically loaded in
            #  the background because the user probably cares about the fact that this
            #  link was loaded.
            5: 'generated',  # User got to this page by typing in the URL bar and selecting an entry
            #  that did not look like a URL.  For example, a match might have the URL
            #  of a Google search result page, but appear like 'Search Google for ...'.
            #  These are not quite the same as TYPED navigations because the user
            #  didn't type or see the destination URL.
            #  See also KEYWORD.
            6: 'start page',  # This is a toplevel navigation. This is any content that is automatically
            #  loaded in a toplevel frame.  For example, opening a tab to show the ASH
            #  screen saver, opening the devtools window, opening the NTP after the safe
            #  browsing warning, opening web-based dialog boxes are examples of
            #  AUTO_TOPLEVEL navigations.
            7: 'form submit',  # The user filled out values in a form and submitted it. NOTE that in
            #  some situations submitting a form does not result in this transition
            #  type. This can happen if the form uses script to submit the contents.
            8: 'reload',  # The user 'reloaded' the page, either by hitting the reload button or by
            #  hitting enter in the address bar.  NOTE: This is distinct from the
            #  concept of whether a particular load uses 'reload semantics' (i.e.
            #  bypasses cached data).  For this reason, lots of code needs to pass
            #  around the concept of whether a load should be treated as a 'reload'
            #  separately from their tracking of this transition type, which is mainly
            #  used for proper scoring for consumers who care about how frequently a
            #  user typed/visited a particular URL.
            #  SessionRestore and undo tab close use this transition type too.
            9: 'keyword',  # The url was generated from a replaceable keyword other than the default
            #  search provider. If the user types a keyword (which also applies to
            #  tab-to-search) in the omnibox this qualifier is applied to the transition
            #  type of the generated url. TemplateURLModel then may generate an
            #  additional visit with a transition type of KEYWORD_GENERATED against the
            #  url 'http://' + keyword. For example, if you do a tab-to-search against
            #  wikipedia the generated url has a transition qualifer of KEYWORD, and
            #  TemplateURLModel generates a visit for 'wikipedia.org' with a transition
            #  type of KEYWORD_GENERATED.
            10: 'keyword generated'}  # Corresponds to a visit generated for a keyword. See description of
        #  KEYWORD for more details.

        qualifiers_friendly = {
            0x00800000: 'Blocked',  # A managed user attempted to visit a URL but was blocked.
            0x01000000: 'Forward or Back',  # User used the Forward or Back button to navigate among browsing
            #  history.
            0x02000000: 'From Address Bar',  # User used the address bar to trigger this navigation.
            0x04000000: 'Home Page',  # User is navigating to the home page.
            0x08000000: 'From API',  # The transition originated from an external application; the exact
            #  definition of this is embedder dependent.
            0x10000000: 'Navigation Chain Start',  # The beginning of a navigation chain.
            0x20000000: 'Navigation Chain End',  # The last transition in a redirect chain.
            0x40000000: 'Client Redirect',  # Redirects caused by JavaScript or a meta refresh tag on the page.
            0x80000000: 'Server Redirect'}  # Redirects sent from the server by HTTP headers. It might be nice to
        #  break this out into 2 types in the future, permanent or temporary,
        #  if we can get that information from WebKit.
        raw = transition
        # If the transition has already been translated to a string, just use that
        if isinstance(raw, str):
            transition_friendly = raw
            return

        core_mask = 0xff
        code = raw & core_mask

        if code in list(transition_friendly.keys()):
            transition_friendly = transition_friendly[code] + '; '

        for qualifier in qualifiers_friendly:
            if raw & qualifier == qualifier:
                if not transition_friendly:
                    transition_friendly = ""
                transition_friendly += qualifiers_friendly[qualifier] + '; '

        return str(transition_friendly)

    def decode_duration(v_duration):
        duration = 'None'
        if v_duration != 0:
            duration = datetime.timedelta(microseconds=v_duration)  # type: timedelta

        return str(duration)

    def decode_source(visit_source):
        # https://code.google.com/p/chromium/codesearch#chromium/src/components/history/core/browser/history_types.h
        source_friendly = {
            0: 'Synced',  # Synchronized from somewhere else.
            1: 'Local',  # User browsed. In my experience, this value isn't written; it will be null.
            None: 'Local',
            # See https://cs.chromium.org/chromium/src/components/history/core/browser/visit_database.cc
            2: 'Added by Extension',  # Added by an extension.
            3: 'Firefox (Imported)',
            4: 'IE (Imported)',
            5: 'Safari (Imported)'}

        raw = visit_source

        if raw in list(source_friendly.keys()):
            visit_source = source_friendly[raw]

        return str(visit_source)

    def decode_download_state(state, received_bytes, total_bytes):
        # from download_item.h on Chromium site
        states = {
            0: "In Progress",  # Download is actively progressing.
            1: "Complete",  # Download is completely finished.
            2: "Cancelled",  # Download has been cancelled.
            3: "Interrupted",  # '3' was the old "Interrupted" code until a bugfix in Chrome v22. 22+ it's '4'
            4: "Interrupted"}  # This state indicates that the download has been interrupted.

        if state in list(states.keys()):
            state_friendly = states[state]
        else:
            state_friendly = "[Error - Unknown State]"

        try:
            status = "%s -  %i%% [%i/%i]" % \
                     (state_friendly, (float(received_bytes) / float(total_bytes)) * 100,
                      received_bytes, total_bytes)
        except ZeroDivisionError:
            status = "%s -  %i bytes" % (state_friendly, received_bytes)
        except:
            status = "[parsing error]"
        status_friendly = status

        return str(status_friendly)

    def decode_interrupt_reason(interrupt_reason):
        interrupts = {
            0: 'No Interrupt',  # Success

            # from download_interrupt_reason_values.h on Chromium site
            # File errors
            1: 'File Error',  # Generic file operation failure.
            2: 'Access Denied',  # The file cannot be accessed due to security restrictions.
            3: 'Disk Full',  # There is not enough room on the drive.
            5: 'Path Too Long',  # The directory or file name is too long.
            6: 'File Too Large',  # The file is too large for the file system to handle.
            7: 'Virus',  # The file contains a virus.
            10: 'Temporary Problem',  # The file was in use. Too many files are opened at once. We have run
            #  out of memory.
            11: 'Blocked',  # The file was blocked due to local policy.
            12: 'Security Check Failed',  # An attempt to check the safety of the download failed due to
            #  unexpected reasons. See http://crbug.com/153212.
            13: 'Resume Error',  # An attempt was made to seek past the end of a file in opening a file
            #  (as part of resuming a previously interrupted download).

            # Network errors
            20: 'Network Error',  # Generic network failure.
            21: 'Operation Timed Out',  # The network operation timed out.
            22: 'Connection Lost',  # The network connection has been lost.
            23: 'Server Down',  # The server has gone down.

            # Server responses
            30: 'Server Error',  # The server indicates that the operation has failed (generic).
            31: 'Range Request Error',  # The server does not support range requests.
            32: 'Server Precondition Error',  # The download request does not meet the specified precondition.
            #  Internal use only:  the file has changed on the server.
            33: 'Unable to get file',  # The server does not have the requested data.
            34: 'Server Unauthorized',  # Server didn't authorize access to resource.
            35: 'Server Certificate Problem',  # Server certificate problem.
            36: 'Server Access Forbidden',  # Server access forbidden.
            37: 'Server Unreachable',  # Unexpected server response. This might indicate that the responding
            #  server may not be the intended server.
            38: 'Content Length Mismatch',
            # The server sent fewer bytes than the content-length header. It may indicate
            #  that the connection was closed prematurely, or the Content-Length header was
            #  invalid. The download is only interrupted if strong validators are present.
            #  Otherwise, it is treated as finished.
            39: 'Cross Origin Redirect',  # An unexpected cross-origin redirect happened.

            # User input
            40: 'Cancelled',  # The user cancelled the download.
            41: 'Browser Shutdown',  # The user shut down the browser.

            # Crash
            50: 'Browser Crashed'}  # The browser crashed.

        if interrupt_reason in list(interrupts.keys()):
            interrupt_reason_friendly = interrupts[interrupt_reason]
        elif interrupt_reason is None:
            interrupt_reason_friendly = None
        else:
            interrupt_reason_friendly = '[Error - Unknown Interrupt Code]'

        return str(interrupt_reason_friendly)

    def decode_danger_type(danger_type):
        # from download_danger_type.h on Chromium site
        dangers = {
            0: 'Not Dangerous',  # The download is safe.
            1: 'Dangerous',  # A dangerous file to the system (e.g.: a pdf or extension from places
            #  other than gallery).
            2: 'Dangerous URL',  # SafeBrowsing download service shows this URL leads to malicious file
            #  download.
            3: 'Dangerous Content',  # SafeBrowsing download service shows this file content as being
            #  malicious.
            4: 'Content May Be Malicious',  # The content of this download may be malicious (e.g., extension is exe
            #  but SafeBrowsing has not finished checking the content).
            5: 'Uncommon Content',  # SafeBrowsing download service checked the contents of the download,
            #  but didn't have enough data to determine whether it was malicious.
            6: 'Dangerous But User Validated',  # The download was evaluated to be one of the other types of danger,
            #  but the user told us to go ahead anyway.
            7: 'Dangerous Host',  # SafeBrowsing download service checked the contents of the download
            #  and didn't have data on this specific file, but the file was served
            #  from a host known to serve mostly malicious content.
            8: 'Potentially Unwanted',  # Applications and extensions that modify browser and/or computer
            #  settings
            9: 'Whitelisted by Policy'}  # Download URL whitelisted by enterprise policy.

        if danger_type in list(dangers.keys()):
            danger_type_friendly = dangers[danger_type]
        elif danger_type is None:
            danger_type_friendly = None
        else:
            danger_type_friendly = '[Error - Unknown Danger Code]'

        return str(danger_type_friendly)

    def decode_opened(opened):
        opened_state = {
            0: 'No',
            1: 'Yes'
        }

        if opened in list(opened_state.keys()):
            opened_friendly = opened_state[opened]
        elif opened is None:
            opened_friendly = None
        else:
            opened_friendly = '[Error - Unknown Interrupt Code]'

        return str(opened_friendly)

    ########################### url, keyword, cloud 파싱 시작 ###################################
    s_cur1.execute(
        "SELECT urls.id, urls.url, urls.title, urls.visit_count, urls.typed_count, urls.last_visit_time, urls.hidden, visits.visit_time, visits.from_visit, visits.visit_duration,visits.transition, visit_source.source FROM urls JOIN visits ON urls.id = visits.url LEFT JOIN visit_source ON visits.id = visit_source.id")

    url = s_cur1.fetchall()

    for row in url:
        url_data_list = ['url', friendly_date(row[5]), row[1], row[2], decode_source(row[11]),
                         decode_duration(row[9]), row[3], row[4], row[6], decode_transition(row[10])]
        url_data_list_2.append(url_data_list)

        google_search = "https://www.google.com/search"
        naver_search = "https://search.naver.com"
        daum_search = "https://search.daum.net"

        if google_search in row[1]:
            keyword_data_list = ['keyword', friendly_date(row[5]), row[2]]
            keyword_data_list_2.append(keyword_data_list)
        elif naver_search in row[1]:
            keyword_data_list = ['keyword', friendly_date(row[5]), row[2]]
            keyword_data_list_2.append(keyword_data_list)
        elif daum_search in row[1]:
            keyword_data_list = ['keyword', friendly_date(row[5]), row[2]]
            keyword_data_list_2.append(keyword_data_list)

        if "onedrive.live.com/?" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "cloud.naver.com/#" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "drive.google.com/drive/u/0/my-drive" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/mail" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/contacts" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/calendar" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/photos" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/iclouddrive" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/notes" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/reminders" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/pages" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/numbers" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/keynote" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)
        elif "icloud.com/find" in row[1]:
            cloud_data_list = [friendly_date(row[5]), row[1], row[2]]
            cloud_data_list_2.append(cloud_data_list)



    ####################### download parsing 시작 ###########################
    s_cur5.execute(
        "SELECT downloads.id, downloads_url_chains.url, downloads.received_bytes, downloads.total_bytes, downloads.state, downloads.target_path, downloads.start_time, downloads.end_time, downloads.opened, downloads.danger_type, downloads.interrupt_reason, downloads.etag, downloads.last_modified, downloads_url_chains.chain_index FROM downloads, downloads_url_chains WHERE downloads_url_chains.id = downloads.id"
    )

    downloads = s_cur5.fetchall()

    def filename(path):
        list = path.split("\\")
        return list[-1]


    for row in downloads:
        if row[12] == '':
            download_data_list = ['download', filename(str(row[5])), friendly_date(row[6]), row[1],
                                  decode_download_state(row[4], row[2], row[3]), row[5],
                                  decode_interrupt_reason(row[10]), decode_danger_type(row[9]), decode_opened(row[8]),
                                  row[11], 'null']
            download_data_list_2.append(download_data_list)
        else:
            download_data_list = ['download', filename(str(row[5])), friendly_date(row[6]), row[1],
                                  decode_download_state(row[4], row[2], row[3]), row[5],
                                  decode_interrupt_reason(row[10]), decode_danger_type(row[9]), decode_opened(row[8]),
                                  row[11], change_last_modified_time(str(row[12]))]
            download_data_list_2.append(download_data_list)

    ########################### autofill 파싱 시작 ###########################
    s_cur2.execute('SELECT autofill.date_last_used, autofill.name, autofill.value, autofill.count FROM autofill')
    autofill = s_cur2.fetchall()

    for row in autofill:
        autofill_data_list = ['autofill', friendly_date(row[0]), row[1], row[2]]
        autofill_data_list_2.append(autofill_data_list)

    ################################ bookmark 파싱 시작 #################################
    bookmarks_path = os.path.join('COPY\\BROWSER', 'Bookmarks')

    with open(bookmarks_path, encoding='utf-8', errors='replace') as f:
        decoded_json = json.loads(f.read())

    bookmark_data_list = []
    bookmark_data_list_2 = []

    def process_bookmark_children(parent, children):
        for child in children:
            if child["type"] == "url":
                bookmark_data_list = ['bookmark', friendly_date(child["date_added"]), child["url"], child["name"],
                                      parent]
                bookmark_data_list_2.append(bookmark_data_list)

    for top_level_folder in list(decoded_json["roots"].keys()):
        if top_level_folder != "sync_transaction_version" and top_level_folder != "synced" and top_level_folder != "meta_info":
            if decoded_json["roots"][top_level_folder]["children"] is not None:
                process_bookmark_children(decoded_json["roots"][top_level_folder]["name"],
                                          decoded_json["roots"][top_level_folder]["children"])

    ########################## Cookies 파싱 시작 #############################
    def decrypt_cookie(encrypted_value):
        """Decryption based on work by Nathan Henrie and Jordan Wright as well as Chromium source:
         - Mac/Linux: http://n8henrie.com/2014/05/decrypt-chrome-cookies-with-python/
         - Windows: https://gist.github.com/jordan-wright/5770442#file-chrome_extract-py
         - Relevant Chromium source code: http://src.chromium.org/viewvc/chrome/trunk/src/components/os_crypt/
         """
        salt = b'saltysalt'
        iv = b' ' * 16
        length = 16

        def chrome_decrypt(encrypted, key=None):
            # Encrypted cookies should be prefixed with 'v10' according to the
            # Chromium code. Strip it off.
            encrypted = encrypted[3:]

            # Strip padding by taking off number indicated by padding
            # eg if last is '\x0e' then ord('\x0e') == 14, so take off 14.
            def clean(x):
                return x[:-ord(x[-1])]

            cipher = AES.new(key, AES.MODE_CBC, IV=iv)
            decrypted = cipher.decrypt(encrypted)

            return clean(decrypted)

        decrypted_value = "<error>"

        if encrypted_value is not None:
            if len(encrypted_value) >= 2:
                try:
                    decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]
                except:
                    decrypted_value = "<encrypted>"
        return decrypted_value

    s_cur3.execute(
        'SELECT cookies.host_key, cookies.path, cookies.name, cookies.value, cookies.creation_utc, cookies.last_access_utc, cookies.expires_utc, cookies.is_secure AS secure, cookies.is_httponly AS httponly, cookies.is_persistent AS persistent,  cookies.has_expires, cookies.priority, cookies.encrypted_value FROM cookies'
    )

    cookies = s_cur3.fetchall()

    for row in cookies:
        cookie_data_list = ['cookies_created', friendly_date(row[4]), str(row[0]) + str(row[1]), row[2],
                            decrypt_cookie(row[12])]
        cookie_data_list_2.append(cookie_data_list)
        if row[4] != row[5]:
            if row[5] != to_datetime(0):
                cookie_data_list = ['cookies_accessed', friendly_date(row[5]), str(row[0]) + str(row[1]), row[2],
                                    decrypt_cookie(row[12])]
                cookie_data_list_2.append(cookie_data_list)

    ###############################login data parsing###############################333
    s_cur4.execute(
        'SELECT origin_url, action_url, username_element, username_value, password_element, password_value, date_created, date_last_used, blacklisted_by_user FROM logins')
    logindata = s_cur4.fetchall()

    for row in logindata:
        if row[8] == 1:
            login_data_list = ['login_blacklist', friendly_date(row[6]), row[0], row[2],
                              '<User chose to /"Never save password/" for this site>', row[4], row[5]]
            login_data_list_2.append(login_data_list)
        elif str(row[3]) is not None:
            if str(row[4]) is not None:
                login_data_list = ['login_username', friendly_date(row[6]), row[1], row[2], row[3], row[4],
                                   row[5]]
                login_data_list_2.append(login_data_list)
            else:
                login_data_list = ['login_username', friendly_date(row[6]), row[1], row[2], row[3], row[4],
                                   row[5]]
                login_data_list_2.append(login_data_list)

    ###################################### preference 파싱 시작 ########################################
    def check_and_append_pref(parent, pref, value=None, description=None):
        # If the preference exists, continue
        if parent.get(pref):
            # If no value is specified, use the value from the preference JSON
            if not value:
                value = parent[pref]
            # Append the preference dict to our results array
            results.append({
                'group': None,
                'name': pref,
                'value': value,
                'description': description
            })

        else:
            results.append({
                'group': None,
                'name': pref,
                'value': '<not present>',
                'description': description
            })

    def check_and_append_pref_and_children(parent, pref, value=None, description=None):
        # If the preference exists, continue
        if parent.get(pref):
            # If no value is specified, use the value from the preference JSON
            if not value:
                value = parent[pref]
            # Append the preference dict to our results array
            results.append({
                'group': None,
                'name': pref,
                'value': value,
                'description': description
            })

        else:
            results.append({
                'group': None,
                'name': pref,
                'value': '<not present>',
                'description': description
            })

    def append_group(group, description=None):
        # Append the preference group to our results array
        results.append({
            'group': group,
            'name': None,
            'value': None,
            'description': description
        })

    def append_pref(pref, value=None, description=None):
        results.append({
            'group': None,
            'name': pref,
            'value': value,
            'description': description
        })

    def expand_language_code(code):
        # From https://cs.chromium.org/chromium/src/components/translate/core/browser/translate_language_list.cc
        codes = {
            'af': 'Afrikaans',
            'am': 'Amharic',
            'ar': 'Arabic',
            'az': 'Azerbaijani',
            'be': 'Belarusian',
            'bg': 'Bulgarian',
            'bn': 'Bengali',
            'bs': 'Bosnian',
            'ca': 'Catalan',
            'ceb': 'Cebuano',
            'co': 'Corsican',
            'cs': 'Czech',
            'cy': 'Welsh',
            'da': 'Danish',
            'de': 'German',
            'el': 'Greek',
            'en': 'English',
            'eo': 'Esperanto',
            'es': 'Spanish',
            'et': 'Estonian',
            'eu': 'Basque',
            'fa': 'Persian',
            'fi': 'Finnish',
            'fy': 'Frisian',
            'fr': 'French',
            'ga': 'Irish',
            'gd': 'Scots Gaelic',
            'gl': 'Galician',
            'gu': 'Gujarati',
            'ha': 'Hausa',
            'haw': 'Hawaiian',
            'hi': 'Hindi',
            'hr': 'Croatian',
            'ht': 'Haitian Creole',
            'hu': 'Hungarian',
            'hy': 'Armenian',
            'id': 'Indonesian',
            'ig': 'Igbo',
            'is': 'Icelandic',
            'it': 'Italian',
            'iw': 'Hebrew',
            'ja': 'Japanese',
            'ka': 'Georgian',
            'kk': 'Kazakh',
            'km': 'Khmer',
            'kn': 'Kannada',
            'ko': 'Korean',
            'ku': 'Kurdish',
            'ky': 'Kyrgyz',
            'la': 'Latin',
            'lb': 'Luxembourgish',
            'lo': 'Lao',
            'lt': 'Lithuanian',
            'lv': 'Latvian',
            'mg': 'Malagasy',
            'mi': 'Maori',
            'mk': 'Macedonian',
            'ml': 'Malayalam',
            'mn': 'Mongolian',
            'mr': 'Marathi',
            'ms': 'Malay',
            'mt': 'Maltese',
            'my': 'Burmese',
            'ne': 'Nepali',
            'nl': 'Dutch',
            'no': 'Norwegian',
            'ny': 'Nyanja',
            'pa': 'Punjabi',
            'pl': 'Polish',
            'ps': 'Pashto',
            'pt': 'Portuguese',
            'ro': 'Romanian',
            'ru': 'Russian',
            'sd': 'Sindhi',
            'si': 'Sinhala',
            'sk': 'Slovak',
            'sl': 'Slovenian',
            'sm': 'Samoan',
            'sn': 'Shona',
            'so': 'Somali',
            'sq': 'Albanian',
            'sr': 'Serbian',
            'st': 'Southern Sotho',
            'su': 'Sundanese',
            'sv': 'Swedish',
            'sw': 'Swahili',
            'ta': 'Tamil',
            'te': 'Telugu',
            'tg': 'Tajik',
            'th': 'Thai',
            'tl': 'Tagalog',
            'tr': 'Turkish',
            'uk': 'Ukrainian',
            'ur': 'Urdu',
            'uz': 'Uzbek',
            'vi': 'Vietnamese',
            'yi': 'Yiddish',
            'xh': 'Xhosa',
            'yo': 'Yoruba',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)',
            'zu': 'Zulu'
        }
        return codes.get(code, code)

    results = []
    timestamped_preference_items = []

    preferences_file = 'COPY\\BROWSER\\Preferences'
    # Open 'Preferences' file

    with open(preferences_file, encoding='utf-8', errors='replace') as f:
        prefs = json.loads(f.read())

    # Account Information
    if prefs.get('account_info'):
        append_group('Account Information')
        for account in prefs['account_info']:
            for account_item in list(account.keys()):
                append_pref(account_item, account[account_item])

    # Local file paths
    append_group('Local file paths')
    if prefs.get('download'):
        check_and_append_pref(prefs['download'], 'default_directory')
    if prefs.get('printing'):
        if prefs.get('print_preview_sticky_settings'):
            check_and_append_pref(prefs['printing']['print_preview_sticky_settings'], 'savePath')
    if prefs.get('savefile'):
        check_and_append_pref(prefs['savefile'], 'default_directory')
    if prefs.get('selectfile'):
        check_and_append_pref(prefs['selectfile'], 'last_directory')

    # Autofill
    if prefs.get('autofill'):
        append_group('Autofill')
        check_and_append_pref(prefs['autofill'], 'enabled')

    # Clearing Chrome Data
    if prefs.get('browser'):
        append_group('Clearing Chrome Data')
        if prefs['browser'].get('last_clear_browsing_data_time'):
            check_and_append_pref(
                prefs['browser'], 'last_clear_browsing_data_time',
                friendly_date(prefs['browser']['last_clear_browsing_data_time']),
                'Last time the history was cleared')
        check_and_append_pref(prefs['browser'], 'clear_lso_data_enabled')
        if prefs['browser'].get('clear_data'):
            check_and_append_pref(
                prefs['browser']['clear_data'], 'time_period',
                description='0: past hour; 1: past day; 2: past week; 3: last 4 weeks; '
                            '4: the beginning of time')
            check_and_append_pref(prefs['browser']['clear_data'], 'content_licenses')
            check_and_append_pref(prefs['browser']['clear_data'], 'hosted_apps_data')
            check_and_append_pref(prefs['browser']['clear_data'], 'cookies')
            check_and_append_pref(prefs['browser']['clear_data'], 'download_history')
            check_and_append_pref(prefs['browser']['clear_data'], 'browsing_history')
            check_and_append_pref(prefs['browser']['clear_data'], 'passwords')
            check_and_append_pref(prefs['browser']['clear_data'], 'form_data')

    append_group('Per Host Zoom Levels', 'These settings persist even when the history is cleared, and may be '
                                         'useful in some cases.')

    # There are per_host_zoom_levels keys in at least two locations: profile.per_host_zoom_levels and
    # partition.per_host_zoom_levels.[integer].
    if prefs.get('profile'):
        if prefs['profile'].get('per_host_zoom_levels'):
            for zoom in list(prefs['profile']['per_host_zoom_levels'].keys()):
                check_and_append_pref(prefs['profile']['per_host_zoom_levels'], zoom)

    if prefs.get('partition'):
        if prefs['partition'].get('per_host_zoom_levels'):
            for number in list(prefs['partition']['per_host_zoom_levels'].keys()):
                for zoom in list(prefs['partition']['per_host_zoom_levels'][number].keys()):
                    check_and_append_pref(prefs['partition']['per_host_zoom_levels'][number], zoom)

    if prefs.get('profile'):
        if prefs['profile'].get('content_settings'):
            if prefs['profile']['content_settings'].get('pattern_pairs'):
                append_group('Profile Content Settings', 'These settings persist even when the history is '
                                                         'cleared, and may be useful in some cases.')
                for pair in list(prefs['profile']['content_settings']['pattern_pairs'].keys()):
                    # Adding the space before the domain prevents Excel from freaking out...  idk.
                    append_pref(' ' + str(pair), str(prefs['profile']['content_settings']['pattern_pairs'][pair]))

            if prefs['profile']['content_settings'].get('exceptions'):
                if prefs['profile']['content_settings']['exceptions'].get('media_engagement'):
                    # Example (from in Preferences file):
                    # "http://obsidianforensics.com:80,*": {
                    #     "last_modified": "13160264938091184",
                    #     "setting": {
                    #         "hasHighScore": false,
                    #         "lastMediaPlaybackTime": 0.0,
                    #         "mediaPlaybacks": 0,
                    #         "visits": 1
                    #     }
                    for origin, pref_data in \
                            prefs['profile']['content_settings']['exceptions']['media_engagement'].items():
                        if pref_data.get('last_modified'):
                            pref_data_list = ['preference', friendly_date(pref_data['last_modified']), origin,
                                              f'media_engagement [in {preferences_file}.profile.content_settings.exceptions]',
                                              str(pref_data)]
                            pref_data_list_2.append(pref_data_list)

                if prefs['profile']['content_settings']['exceptions'].get('notifications'):
                    # Example (from in Preferences file):
                    # "https://www.youtube.com:443,*": {
                    #     "last_modified": "13161568350592864",
                    #     "setting": 1
                    # }
                    for origin, pref_data in \
                            prefs['profile']['content_settings']['exceptions']['notifications'].items():
                        if pref_data.get('last_modified'):
                            pref_data_list = ['preference', friendly_date(pref_data['last_modified']), origin,
                                              f'notification [in {preferences_file}.profile.content_settings.exceptions]',
                                              str(pref_data)]
                            pref_data_list_2.append(pref_data_list)

                if prefs['profile']['content_settings']['exceptions'].get('permission_autoblocking_data'):
                    # Example (from in Preferences file):
                    # "https://www.mapquest.com:443,*": {
                    #     "last_modified": "13161750781018557",  # This can be 0, or not exist at all
                    #       "setting": {
                    #           "Geolocation": {
                    #               "ignore_count": 1
                    #  }}},
                    for origin, pref_data in \
                            prefs['profile']['content_settings']['exceptions'][
                                'permission_autoblocking_data'].items():
                        if pref_data.get('last_modified') and pref_data.get('last_modified') != '0':
                            pref_data_list = ['preference', friendly_date(pref_data['last_modified']), origin,
                                              f'permission_autoblocking_data [in {preferences_file}.profile.content_settings.exceptions]',
                                              str(pref_data)]
                            pref_data_list_2.append(pref_data_list)

                if prefs['profile']['content_settings']['exceptions'].get('site_engagement'):
                    # Example (from in Preferences file):
                    # "http://aboutdfir.com:80,*": {
                    #     "last_modified": "13162626153701643",
                    #     "setting": {
                    #         "lastEngagementTime": 13162626153701620.0,
                    #         "lastShortcutLaunchTime": 0.0,
                    #         "pointsAddedToday": 4.5,
                    #         "rawScore": 4.5
                    #     }
                    for origin, pref_data in \
                            prefs['profile']['content_settings']['exceptions']['site_engagement'].items():
                        if pref_data.get('last_modified'):
                            pref_data_list = ['preference', friendly_date(pref_data['last_modified']), origin,
                                              f'site_engagement [in {preferences_file}.profile.content_settings.exceptions]',
                                              str(pref_data)]
                            pref_data_list_2.append(pref_data_list)

                if prefs['profile']['content_settings']['exceptions'].get('sound'):
                    # Example (from in Preferences file):
                    # "http://obsidianforensics.com:80,*": {
                    #     "last_modified": "13162624224060055",
                    #     "setting": 2
                    # }
                    for origin, pref_data in \
                            prefs['profile']['content_settings']['exceptions']['sound'].items():
                        if pref_data.get('last_modified'):
                            interpretation = ''
                            if pref_data.get('setting') == 2:
                                interpretation = 'Muted site'
                                pref_data_list = ['preference', friendly_date(pref_data['last_modified']), origin,
                                                  f'sound [in {preferences_file}.profile.content_settings.exceptions]',
                                                  str(pref_data)]
                                pref_data_list_2.append(pref_data_list)

    if prefs.get('extensions'):
        if prefs['extensions'].get('autoupdate'):
            # Example (from in Preferences file):
            # "extensions": {
            #     ...
            #     "autoupdate": {
            #         "last_check": "13162668769688981",
            #         "next_check": "13162686093672995"
            #     },
            if prefs['extensions']['autoupdate'].get('last_check'):
                pref_data_list = ['preference', friendly_date(pref_data['extensions']['autoupdate']['last_check']),
                                  origin,
                                  f'autoupdate.last_check [in {preferences_file}..extensions]',
                                  prefs['extensions']['autoupdate']['last_check']]
                pref_data_list_2.append(pref_data_list)

    if prefs.get('signin'):
        if prefs['signin'].get('signedin_time'):
            # Example (from in Preferences file):
            # "signin": {
            #     "signedin_time": "13196354823425155"
            #  },
            pref_data_list = ['preference', friendly_date(prefs['signin']['signedin_time']), origin,
                              f'signedin_time [in {preferences_file}.signin]', prefs['signin']['signedin_time']]
            pref_data_list_2.append(pref_data_list)

    if prefs.get('translate_last_denied_time_for_language'):
        for lang_code, timestamp in prefs['translate_last_denied_time_for_language'].items():
            # Example (from in Preferences file):
            # "translate_last_denied_time_for_language": {
            #   u'ar': 1438733440742.06,
            #   u'th': [1447786189498.162],
            #   u'hi': 1438798234384.275,
            #  },
            if isinstance(timestamp, list):
                timestamp = timestamp[0]
            assert isinstance(timestamp, float)
            pref_data_list = ['preference', friendly_date(pref_data['last_modified']), origin,
                              f'translate_last_denied_time_for_lauguage [in {preferences_file}]',
                              f'{lang_code} : {timestamp}']
            pref_data_list_2.append(pref_data_list)



    Database.browser_db_insert(url_data_list_2, autofill_data_list_2, bookmark_data_list_2, cookie_data_list_2,
                                login_data_list_2, pref_data_list_2, keyword_data_list_2, download_data_list_2, cloud_data_list_2)

    CacheParser.get_cache('Cache', 'Cache')
    CacheParser.get_cache('cache', 'GPUCache')

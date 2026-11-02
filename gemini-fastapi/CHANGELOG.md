# Changelog

> [!NOTE]
> If you find this addon useful, please consider giving it a ⭐ on [GitHub](https://github.com/luuquangvu/ha-addons) to support my work and help others discover it. Thank you very much! ❤️

## 1.0.126 - 2026-11-02

- Update version to 20261102-bab0e35
- Cập nhật phiên bản lên 20261102-bab0e35

## 1.0.125 - 2026-11-02

- Update version to 20261102-b194eb6
- Cập nhật phiên bản lên 20261102-b194eb6

## 1.0.124 - 2026-11-02

- Update version to 20261102-b194eb6
- Cập nhật phiên bản lên 20261102-b194eb6

## 1.0.123 - 2026-11-01

- **Configuration is now in the App's Configuration tab.** You no longer need to edit `config.yaml`. Enter your cookies and API key in the App.
- **Cấu hình giờ nằm trong tab Cấu hình của App.** Bạn không cần chỉnh sửa `config.yaml` nữa. Hãy nhập cookie và API key ngay trong App.
- **One-time migration.** On the first start after updating, the App removes the old `/homeassistant/gemini-fastapi/config` folder and moves your conversations to its own `/data` storage. If no account is configured yet, the App starts in guest mode: add your cookies and API key in the Configuration tab and restart it.
- **Di chuyển một lần.** Ở lần khởi động đầu tiên sau khi cập nhật, App sẽ xóa thư mục cấu hình cũ `/homeassistant/gemini-fastapi/config` và chuyển hội thoại sang vùng lưu trữ `/data` riêng. Nếu chưa có tài khoản, App sẽ khởi động ở chế độ khách: hãy nhập cookie và API key trong tab Cấu hình rồi khởi động lại.
- **Multiple Gemini accounts.** Add more than one account to share requests and reduce rate limits. Each account can use its own proxy.
- **Nhiều tài khoản Gemini.** Thêm nhiều tài khoản để chia sẻ yêu cầu và giảm giới hạn tần suất. Mỗi tài khoản có thể dùng proxy riêng.
- **Both cookies are required.** Each account needs `__Secure-1PSID` and `__Secure-1PSIDTS`. With no account, the App runs in guest mode: text works, but there is no conversation history, file uploads, or model choice.
- **Bắt buộc cả hai cookie.** Mỗi tài khoản cần `__Secure-1PSID` và `__Secure-1PSIDTS`. Nếu chưa có tài khoản, App chạy ở chế độ khách: vẫn trả lời văn bản nhưng không có lịch sử hội thoại, không tải tệp lên và không chọn được mô hình.
- **Automatic client IDs are based on the account cookie.** They stay the same when you reorder or remove accounts, but change if the `1PSID` cookie changes. To keep an old conversation, set its previous client ID (for example `client-id-1`) explicitly.
- **ID client tự động dựa trên cookie tài khoản.** ID không đổi khi bạn đổi thứ tự hoặc xóa tài khoản, nhưng sẽ đổi nếu cookie `1PSID` thay đổi. Để giữ hội thoại cũ, hãy đặt rõ ID client trước đây (ví dụ `client-id-1`).
- **Only the options in the Configuration tab can be changed.** Other upstream `config.yaml` settings use their defaults.
- **Chỉ các tùy chọn trong tab Cấu hình là có thể thay đổi.** Các cài đặt khác trong `config.yaml` của upstream sẽ dùng giá trị mặc định.
- **`/homeassistant` is only used for this one-time migration.** If it is unavailable, the App still starts and tries again next time.
- **`/homeassistant` chỉ được dùng cho lần di chuyển một lần này.** Nếu không khả dụng, App vẫn khởi động và thử lại ở lần sau.

## 1.0.122 - 2026-10-30

- Update version to 20261029-323aa90
- Cập nhật phiên bản lên 20261029-323aa90

## 1.0.121 - 2026-10-28

- Update version to 20261028-1ff566c
- Cập nhật phiên bản lên 20261028-1ff566c

## 1.0.120 - 2026-10-18

- Update version to 20261017-6f34e15
- Cập nhật phiên bản lên 20261017-6f34e15

## 1.0.119 - 2026-10-01

- Update version to 20261001-2e719d6
- Cập nhật phiên bản lên 20261001-2e719d6

## 1.0.118 - 2026-08-28

- Update version to 20260828-66dc3f7
- Cập nhật phiên bản lên 20260828-66dc3f7

## 1.0.117 - 2026-08-27

- Update version to 20260827-23565b1
- Cập nhật phiên bản lên 20260827-23565b1

## 1.0.116 - 2026-08-27

- Update version to 20260827-9477187
- Cập nhật phiên bản lên 20260827-9477187

## 1.0.115 - 2026-08-26

- Update version to 20260826-c17e912
- Cập nhật phiên bản lên 20260826-c17e912

## 1.0.114 - 2026-08-19

- Update version to 20260819-7d1744e
- Cập nhật phiên bản lên 20260819-7d1744e

## 1.0.113 - 2026-08-17

- Resolve the missing uv command
- Khắc phục lỗi thiếu lệnh uv

## 1.0.112 - 2026-08-17

- Update version to 20260817-24ab2f0
- Cập nhật phiên bản lên 20260817-24ab2f0

## 1.0.111 - 2026-08-17

- Update version to 20260817-2c3cbe5
- Cập nhật phiên bản lên 20260817-2c3cbe5

## 1.0.110 - 2026-08-16

- Update version to 20260816-4464d63
- Cập nhật phiên bản lên 20260816-4464d63

## 1.0.109 - 2026-08-15

- Update version to 20260815-dfcca63
- Cập nhật phiên bản lên 20260815-dfcca63

## 1.0.108 - 2026-08-15

- Update version to 20260815-09f3204
- Cập nhật phiên bản lên 20260815-09f3204

## 1.0.107 - 2026-08-13

- Update version to 20260813-c8e0a83
- Cập nhật phiên bản lên 20260813-c8e0a83

## 1.0.106 - 2026-08-13

- Update version to 20260813-261030c
- Cập nhật phiên bản lên 20260813-261030c

## 1.0.105 - 2026-08-13

- Update version to 20260813-40225eb
- Cập nhật phiên bản lên 20260813-40225eb

## 1.0.104 - 2026-08-12

- Update version to 20260812-01fe60a
- Cập nhật phiên bản lên 20260812-01fe60a

## 1.0.103 - 2026-08-01

- Update version to 20260801-7b2b32f
- Cập nhật phiên bản lên 20260801-7b2b32f

## 1.0.102 - 2026-07-29

- Update version to 20260729-62f159b
- Cập nhật phiên bản lên 20260729-62f159b

## 1.0.101 - 2026-07-29

- Update version to 20260729-0327f99
- Cập nhật phiên bản lên 20260729-0327f99

## 1.0.100 - 2026-05-28

- Update version to 20260528-a1d9c53
- Cập nhật phiên bản lên 20260528-a1d9c53

## 1.0.99 - 2026-05-25

- Update version to 20260525-3816709
- Cập nhật phiên bản lên 20260525-3816709

## 1.0.98 - 2026-05-25

- Update version to 20260525-c448cfb
- Cập nhật phiên bản lên 20260525-c448cfb

## 1.0.97 - 2026-05-25

- Update version to 20260525-c0b59d9
- Cập nhật phiên bản lên 20260525-c0b59d9

## 1.0.96 - 2026-05-23

- Update version to 20260522-103606c
- Cập nhật phiên bản lên 20260522-103606c

## 1.0.95 - 2026-05-22

- Update version to 20260522-04abb9b
- Cập nhật phiên bản lên 20260522-04abb9b

## 1.0.94 - 2026-05-21

- Update version to 20260521-90fb370
- Cập nhật phiên bản lên 20260521-90fb370

## 1.0.93 - 2026-05-21

- Update version to 20260521-ad11981
- Cập nhật phiên bản lên 20260521-ad11981

## 1.0.92 - 2026-05-21

- Update version to 20260521-228ca5e
- Cập nhật phiên bản lên 20260521-228ca5e

## 1.0.91 - 2026-05-08

- Update version to 20260507-a2f1ebd
- Cập nhật phiên bản lên 20260507-a2f1ebd

## 1.0.90 - 2026-04-28

- Update version to 20260428-9d56d33
- Cập nhật phiên bản lên 20260428-9d56d33

## 1.0.89 - 2026-04-25

- Update version to 20260425-b8cd546
- Cập nhật phiên bản lên 20260425-b8cd546

## 1.0.88 - 2026-04-16

- Update version to 20260416-d6aef65
- Cập nhật phiên bản lên 20260416-d6aef65

## 1.0.87 - 2026-04-15

- Update version to 20260415-e9c7ca7
- Cập nhật phiên bản lên 20260415-e9c7ca7

## 1.0.86 - 2026-04-15

- Update version to 20260415-90aefdb
- Cập nhật phiên bản lên 20260415-90aefdb

## 1.0.85 - 2026-04-14

- Update version to 20260414-506c78f
- Cập nhật phiên bản lên 20260414-506c78f

## 1.0.84 - 2026-04-14

- Update version to 20260414-df512c3
- Cập nhật phiên bản lên 20260414-df512c3

## 1.0.83 - 2026-04-14

- Update version to 20260413-19739e9
- Cập nhật phiên bản lên 20260413-19739e9

## 1.0.82 - 2026-04-09

- Update version to 20260408-b1773c2
- Cập nhật phiên bản lên 20260408-b1773c2

## 1.0.81 - 2026-04-03

- Update version to 20260402-2ca6339
- Cập nhật phiên bản lên 20260402-2ca6339

## 1.0.80 - 2026-03-27

- Update version to 20260326-44968c9
- Cập nhật phiên bản lên 20260326-44968c9

## 1.0.79 - 2026-03-24

- Update version to 20260324-cd402d8
- Cập nhật phiên bản lên 20260324-cd402d8

## 1.0.78 - 2026-03-22

- Update version to 20260321-ccbd7bb
- Cập nhật phiên bản lên 20260321-ccbd7bb

## 1.0.77 - 2026-03-20

- Update version to 20260320-c3730ca
- Cập nhật phiên bản lên 20260320-c3730ca

## 1.0.76 - 2026-03-19

- Update upstream image to 20260319-6a0f99b

## 1.0.75 - 2026-03-19

- Please postpone updating to this version and wait for the next release.
- Vui lòng hoãn cập nhật lên phiên bản này và chờ bản phát hành tiếp theo.

## 1.0.74 - 2026-03-19

- Please postpone updating to this version and wait for the next release.
- Vui lòng hoãn cập nhật lên phiên bản này và chờ bản phát hành tiếp theo.

## 1.0.73 - 2026-03-18

- Update upstream image to 20260318-3a68e96

## 1.0.72 - 2026-03-15

- Update upstream image to 20260314-b929c69

## 1.0.71 - 2026-03-13

- Update upstream image to 20260313-a596009

## 1.0.70 - 2026-03-13

- Update upstream image to 20260312-f1de210

## 1.0.69 - 2026-03-12

- Update upstream image to 20260312-00895cb

## 1.0.68 - 2026-03-11

- Update upstream image to 20260311-2d3cf20

## 1.0.67 - 2026-03-11

- Update upstream image to 20260311-f4b319c

## 1.0.66 - 2026-03-11

- Update upstream image to 20260311-7828a4a

## 1.0.65 - 2026-03-10

- Update upstream image to 20260310-ddc2257

## 1.0.64 - 2026-03-09

- Update upstream image to 20260308-bd24c53

## 1.0.63 - 2026-03-07

- Update upstream image to 20260307-9dfc866

## 1.0.62 - 2026-03-07

- Update upstream image to 20260307-d6920ff

## 1.0.61 - 2026-03-06

- Update upstream image to 20260306-d92fa8f

## 1.0.60 - 2026-03-05

- Update upstream image to 20260304-ece7e7a

## 1.0.59 - 2026-03-04

- Update upstream image to 20260304-d858c2b

## 1.0.58 - 2026-03-04

- Update upstream image to 20260303-ca4475a

## 1.0.57 - 2026-03-03

- Update upstream image to 20260302-43f15c9

## 1.0.56 - 2026-03-02

- Update upstream image to 20260301-e4da69e

## 1.0.55 - 2026-03-01

- Update upstream image to 20260228-ab706d8

## 1.0.54 - 2026-02-28

- Update upstream image to 20260227-1c7f99a

## 1.0.53 - 2026-02-27

- Update upstream image to 20260226-c9693bd

## 1.0.52 - 2026-02-26

- Update upstream image to 20260225-e00a8fa

## 1.0.51 - 2026-02-25

- Update upstream image to 20260224-c4aefbf

## 1.0.50 - 2026-02-24

- Update upstream image to 20260223-fbe19db

## 1.0.49 - 2026-02-23

- Update upstream image to 20260222-6c5cabd

## 1.0.48 - 2026-02-22

- Update upstream image to 20260222-ef058d4

## 1.0.47 - 2026-02-22

- Update upstream image to 20260222-1da4dac

## 1.0.46 - 2026-02-18

- Update upstream image to sha256:0de1247d1fb5...

## 1.0.45 - 2026-02-14

- Update upstream image to sha256:8b3af38c51aa...

## 1.0.44 - 2026-02-14

- Update upstream image to sha256:7b7e1652c2c2...

## 1.0.43 - 2026-02-13

- Update upstream image to sha256:a142dbd25dbd...

## 1.0.42 - 2026-02-12

- Update upstream image to sha256:2d0fc60367df...

## 1.0.41 - 2026-02-10

- Update upstream image to sha256:83db4cdfe69b...

## 1.0.40 - 2026-02-10

- Update upstream image to sha256:6416d8f19ca0...

## 1.0.39 - 2026-02-10

- Update upstream image to sha256:7d691eba6ff0...

## 1.0.38 - 2026-02-09

- Update upstream image to sha256:f3212039f9b0...

## 1.0.37 - 2026-02-08

- Update upstream image to sha256:11d5168f42d2...

## 1.0.36 - 2026-02-07

- Update upstream image to sha256:7829f079b051...

## 1.0.35 - 2026-02-06

- Update upstream image to sha256:d2696e896868...

## 1.0.34 - 2026-02-05

- Update upstream image to sha256:252a0470b344...

## 1.0.33 - 2026-02-05

- Update upstream image to sha256:945089004bd5...

## 1.0.32 - 2026-02-04

- Update upstream image to sha256:f3a116409987...

## 1.0.31 - 2026-02-04

- Update upstream image to sha256:3108fdb495b7...

## 1.0.30 - 2026-02-04

- Update upstream image to sha256:a405d4033e8c...

## 1.0.29 - 2026-02-04

- Update upstream image to sha256:732c9a6863d1...

## 1.0.28 - 2026-02-03

- Update upstream image to sha256:19d1bd634ec8...

## 1.0.27 - 2026-02-03

- Update upstream image to sha256:c4352e05a208...

## 1.0.26 - 2026-01-27

- Update upstream image to sha256:8035dafc6f19...

## 1.0.25 - 2026-01-24

- Update upstream image to sha256:520e185923da...

## 1.0.24 - 2026-01-24

- Update upstream image to sha256:133ab

## 1.0.23 - 2026-01-15

- Fix: Ensure persistent storage is accessible, handle user permissions and resolve the expired cookies issue.

## 1.0.0 - 2025-11-05

- Initial release of Gemini FastAPI add-on.

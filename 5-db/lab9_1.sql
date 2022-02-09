use lab1;
go

OPEN SYMMETRIC KEY SymmetricKey1
DECRYPTION BY CERTIFICATE Certificate1;
GO
-- Читання розшифрованих даних
SELECT
*,
CONVERT(varchar, DecryptByKey(security_code))
AS 'Decrypted security code'
FROM Rooms 
where RoomID > 30;


CLOSE SYMMETRIC KEY SymmetricKey1;
GO
% Dla ka�dej grupy klastr�w znajduje element znajduj�cy sie najbli�ej
% centrum klastra i sprawdza jaka powinna by� klasa danego elementu. Zwraca
% wektor klas o d�ugo�ci r�wnej ilo�ci grup

function [classVect] = getClassesFromGroupsMembers(groups, C, X, Y)

    classVect = [];
    for i=1:size(groups,2)
        group = groups{i};  
        minDist = 99999;
        for j=1:size(group,1)
            dist = norm(C(i,:)-group(j,:));
            if dist < minDist
                minDist = dist;
                closestVector = group(j,:);
            end        
        end
        for k = 1:size(X,1)
            if X(k,:) == closestVector;
                closestVectrClass = Y(k);
                break;
            end
        end
        classVect = [classVect; closestVectrClass];
    end

end